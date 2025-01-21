function Get-SID {
    param (
        [string]$UserName
    )

    if (-not $UserName) {
        $whoami = whoami
        $UserName = $whoami.split('\\')[1]
    }

    $localUser = Get-LocalUser -Name $UserName -ErrorAction SilentlyContinue
    if (-not $localUser) {
        Write-Host -ForegroundColor Red "$UserName doesn't exist in your Windows system!"
        return
    }

    try {
        
        $SID = $localUser.SID
        Write-Host -ForegroundColor Green "Your User: $UserName -- SID: $SID"
    }
    catch {
        Write-Host -ForegroundColor Red "Error: Unable to retrieve SID for user $UserName. Ensure the user exists and is local."
    }
}
