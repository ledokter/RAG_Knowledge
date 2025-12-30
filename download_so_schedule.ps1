$url = "https://archive.org/download/stackexchange/stackoverflow.com-Posts.7z"
$destPath = "D:\RAG_Knowledge\StackOverflow\stackoverflow.com-Posts.7z"
$startTime = "01:00"
$endTime = "05:00"

Write-Host "Monitoring time for download window ($startTime - $endTime)..."

while ($true) {
    $now = Get-Date
    
    # Check if we are in the 1AM - 5AM window
    if ($now.Hour -ge 1 -and $now.Hour -lt 5) {
        Write-Host "Time is $($now.ToString('HH:mm')). Inside window. Starting/Resuming download..."
        
        # Use BITS for resumable download
        $jobName = "StackOverflowDump"
        $job = Get-BitsTransfer -Name $jobName -ErrorAction SilentlyContinue
        
        if ($null -eq $job) {
            # Start new if file doesn't exist or we want to ensure we have the job
            if (-not (Test-Path $destPath)) {
                Start-BitsTransfer -Source $url -Destination $destPath -DisplayName $jobName -Asynchronous -Priority Foreground
                Write-Host "Download started."
            } else {
                 Write-Host "File exists. Assuming resume logic or manual check needed."
                 # For simplicity, we assume if job is gone but file exists, it might be done or broken.
                 # Relaunching BITS on same file usually handles resume if server supports it.
                 Start-BitsTransfer -Source $url -Destination $destPath -DisplayName $jobName -Asynchronous -Priority Foreground
            }
        } else {
             # Resume if suspended/error
             if ($job.JobState -eq 'Suspended' -or $job.JobState -eq 'Error') {
                Resume-BitsTransfer -BitsJob $job -Asynchronous
                Write-Host "Download resumed."
             }
        }
        
        # Monitor loop
        do {
            $current = Get-Date
            $jobStatus = Get-BitsTransfer -Name $jobName -ErrorAction SilentlyContinue
            
            if ($null -eq $jobStatus) {
                Write-Host "Download appeared to finish (job gone)."
                break
            }
            if ($jobStatus.JobState -eq 'Transferred') {
                Complete-BitsTransfer -BitsJob $jobStatus
                Write-Host "Download complete and finalized."
                exit
            }
            if ($jobStatus.JobState -eq 'TransientError') {
                 Write-Warning "Transient error in BITS. Retrying..."
                 Resume-BitsTransfer -BitsJob $jobStatus -Asynchronous
            }

            $percent = 0
            if ($jobStatus.BytesTotal -gt 0) {
                $percent = [math]::Round(($jobStatus.BytesTransferred / $jobStatus.BytesTotal * 100), 2)
            }
            
            Write-Host "Downloading... Status: $($jobStatus.JobState) - $percent% - Time: $($current.ToString('HH:mm'))"
            Start-Sleep -Seconds 60
            
        } while ($current.Hour -ge 1 -and $current.Hour -lt 5)
        
        # If we exited loop because of time
        $current = Get-Date
        if ($current.Hour -ge 5) {
            Write-Host "Time window ended. Suspending download."
            Get-BitsTransfer -Name $jobName | Suspend-BitsTransfer
        }
        
    } else {
        Write-Host "Outside window ($($now.ToString('HH:mm'))). Waiting..."
        Start-Sleep -Seconds 60
    }
}
