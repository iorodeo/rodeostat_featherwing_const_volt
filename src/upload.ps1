$driveLabel = Get-Volume -FileSystemLabel CIRCUITPY
$driveLetter = $driveLabel.DriveLetter
$drivePath = $driveLetter + ":\"
$driveGlob = $drivePath + "*"

Remove-Item -Path $driveGlob -Include *.pcf -verbose
Remove-Item -Path $driveGlob -Include *.py  -verbose

Copy-Item -Path *.py  -Destination $drivePath -verbose
Copy-Item -Path *.pcf -Destination $drivePath -verbose

