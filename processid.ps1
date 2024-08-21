function Get-PID {
    param([string]$Process)

    try {
       
        if ($Process.ToLower().EndsWith(".exe")) {
            $Process = $Process.Replace(".exe", "")
        }

        $running_processes = Get-Process -Name $Process
        
        if ($running_processes) {
            Write-Output "$Process Found!"
            
            $choice = Read-Host "Do you want a unique PID? (Y/N)"
            $c = $choice.ToLower()

            if ($c -eq "y" -or $c -eq "yes") {
                # Displaying only one PID (first instance)
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
            Write-Output "[-] No processes found with the name '$Process'. [-]"
        }
    } catch {
        Write-Host "[-] Error occurred: $_ [-]"
    }
}
