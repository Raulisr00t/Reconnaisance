$interface = Read-Host "Please enter an interface"
$interfaces = Get-NetIPAddress | Select-Object -ExpandProperty InterfaceAlias | ForEach-Object { $_.ToLower() }

if ($interface -and $interfaces -contains $interface.ToLower()) {
    $interface = $interface.ToLower()
    $ip_address = Get-NetIPAddress -InterfaceAlias $interface | Where-Object { $_.AddressFamily -eq "IPv4" } | Select-Object -ExpandProperty IPAddress

    if ($ip_address) {
        $ip_parts = $ip_address -split '\.'

        $base_ip = "$($ip_parts[0]).$($ip_parts[1]).$($ip_parts[2])."
        $ping_results = @()

        for ($i = 1; $i -le 254; $i++) {
            $current_ip = "$base_ip$i"
            $ping_result = Test-Connection -Count 1 -ComputerName $current_ip -Quiet

            if ($ping_result) {
                $ping_results += "[+] $current_ip is up"
            } else {
                $ping_results += "[-] $current_ip is down"
            }
        }

        $ping_results | ForEach-Object { Write-Output $_ }
    } else {
        Write-Output "[-] No IPv4 address found for $interface"
    }
} else {
    Write-Output "[-] Interface not found: $interface"
}
