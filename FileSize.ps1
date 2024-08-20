function Get-FileSize {
    param([string]$path)

    try {
        if (Test-Path -Path $path) {
            $file = Get-Item -Path $path -ErrorAction Stop -Force
            Write-Output "Directory Name: $($file.DirectoryName)"

            $fileSizeBytes = $file.Length
            $sizeUnits = @("Bytes", "KB", "MB", "GB", "TB", "PB", "EB")
            $unitIndex = 0

            while ($fileSizeBytes -ge 1024 -and $unitIndex -lt $sizeUnits.Length - 1) {
                $fileSizeBytes = $fileSizeBytes / 1024
                $unitIndex++
            }

            $fileSizeRounded = [math]::Round($fileSizeBytes, 2)
            Write-Output "File Size: $fileSizeRounded $($sizeUnits[$unitIndex])"
        } else {
            Write-Output "Path does not exist."
        }
    } catch {
        Write-Output "An error occurred: $_"
    }
}
