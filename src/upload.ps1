$circuitpyDrive = Get-Volume -FileSystemLabel CIRCUITPY 
$circuitpyDriveLetter = $circuitpyDrive.DriveLetter

Remove-Item -Path $circuitpyDriverLetter -Include "*.py"
Remove-Item -Path $circuitpyDriverLetter -Include "*.pcf"

Copy-Item -Path "*.py"  -Destination $circuitpyDriveLetter -verbose
Copy-Item -Path "*.pcf" -Destination $circuitpyDriveLetter -verbose
