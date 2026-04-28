# IMPORTANT: Before releasing this package, copy/paste the next 2 lines into PowerShell to remove all comments from this file:
#   $f='c:\path\to\thisFile.ps1'
#   gc $f | ? {$_ -notmatch "^\s*#"} | % {$_ -replace '(^.*?)\s*?[^``]#.*','$1'} | Out-File $f+".~" -en utf8; mv -fo $f+".~" $f

## NOTE: In 80-90% of the cases (95% with licensed versions due to Package Synchronizer and other enhancements),
## AutoUninstaller should be able to detect and handle registry uninstalls without a chocolateyUninstall.ps1.
## See https://docs.chocolatey.org/en-us/choco/commands/uninstall
## and https://docs.chocolatey.org/en-us/create/functions/uninstall-chocolateypackage

## If this is an MSI, ensure 'softwareName' is appropriate, then clean up comments and you are done.
## If this is an exe, change fileType, silentArgs, and validExitCodes

$ErrorActionPreference = 'Stop' # stop on all errors
$packageArgs = @{
    packageName    = $env:ChocolateyPackageName
    softwareNames  = @('VCF 生成器 Lite', 'VCF Generator Lite')
    fileType       = 'EXE'
    silentArgs     = '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-'
    validExitCodes = @(0) 
}

$foundKeys = @()
foreach ($softwareName in $packageArgs['softwareNames']) {
    [array]$keys = Get-UninstallRegistryKey -SoftwareName $softwareName
    if ($keys.Count -gt 0) {
        $foundKeys += $keys
    }
}

if ($foundKeys.Count -eq 1) {
    $foundKeys | ForEach-Object {
        $packageArgs['file'] = "$($_.UninstallString)" #NOTE: You may need to split this if it contains spaces, see below
        Uninstall-ChocolateyPackage @packageArgs
    }
}
elseif ($foundKeys.Count -eq 0) {
    Write-Warning "$packageName has already been uninstalled by other means."
}
elseif ($foundKeys.Count -gt 1) {
    Write-Warning "$($foundKeys.Count) matches found!"
    Write-Warning "To prevent accidental data loss, no programs will be uninstalled."
    Write-Warning "Please alert package maintainer the following keys were matched:"
    $foundKeys | ForEach-Object { Write-Warning "- $($_.DisplayName)" }
}
