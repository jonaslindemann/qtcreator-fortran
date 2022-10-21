[Setup]
AppName=Fortran extensions for Qt Creator
AppVersion=1.1
WizardStyle=modern
DefaultDirName={userappdata}\QtProject\qtcreator
Compression=lzma2
SolidCompression=yes
OutputDir=windows-installer
SignTool=signtool_lu
SignedUninstaller=yes
PrivilegesRequired=lowest

[Files]
Source: "..\generic-highlighter\*"; DestDir: "{app}\generic-highlighter"; Flags: ignoreversion recursesubdirs createallsubdirs; 
Source: "..\templates\*"; DestDir: "{app}\templates"; Flags: ignoreversion recursesubdirs createallsubdirs; 

