function Get-PID {
    param([string]$process)

    try {
        $running_processes = Get-Process -Name $process
        
        if ($running_processes) {
            Write-Output "$process Found!"
            
            $choice = Read-Host "Do you want a unique PID? (Y/N)"
            $c = $choice.ToLower()

            if ($c -eq "y" -or $c -eq "yes") {
         
                $uniquePID = ($running_processes | Select-Object -First 1 -ExpandProperty Id)
                Write-Output "[+] Unique PID is: $uniquePID [+]"
            } 
            elseif ($c -eq "n" -or $c -eq "no") {
                # Displaying all PIDs for the process
                $allPIDs = $running_processes | Select-Object -ExpandProperty Id
                Write-Output "[+] All PIDs are: $($allPIDs -join ', ') [+]"
            } else {
                Write-Output "[-] Invalid choice. Please enter Y or N. [-]"
            }
        } else {
            Write-Output "[-] No processes found with the name '$process'. [-]"
        }
    } catch {
        Write-Host "[-] Error occurred: $_ [-]"
    }
}
