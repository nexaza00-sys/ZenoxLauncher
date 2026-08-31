; ============================================================
;  ZENOX GD LAUNCHER  -  Inno Setup Installer Script v2.0
;  Created by SONI
;  
;  Requires: Inno Setup 6.x  (https://jrsoftware.org/isdl.php)
;  Build the exe first:  run build.bat  or  pyinstaller --onefile main.py
; ============================================================

#define AppName       "ZenoxGD Launcher"
#define AppVersion    "1.0.0"
#define AppPublisher  "SONI"
#define AppURL        "https://github.com/soni/zenoxgd-launcher"
#define AppExeName    "ZenoxGD Launcher.exe"
#define AppCopyright  "Copyright (C) 2024-2026 SONI"
#define AppGUID       "{B14AED00-FF22-5500-E5FF-008814AED0FF}"

[Setup]
; ── Identity ──────────────────────────────────────────────
AppId={{#AppGUID}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
AppCopyright={#AppCopyright}

; ── Version info embedded in exe ──────────────────────────
VersionInfoVersion={#AppVersion}
VersionInfoCompany={#AppPublisher}
VersionInfoDescription={#AppName} Setup
VersionInfoCopyright={#AppCopyright}
VersionInfoProductName={#AppName}
VersionInfoProductVersion={#AppVersion}

; ── Paths ─────────────────────────────────────────────────
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputDir=Output
OutputBaseFilename=ZenoxGD_Launcher_Setup_v{#AppVersion}
SetupIconFile=assets\icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

; ── Privileges ────────────────────────────────────────────
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; ── Architecture ──────────────────────────────────────────
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; ── Uninstall ─────────────────────────────────────────────
UninstallDisplayName={#AppName}
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayVersion={#AppVersion}
UninstallURL={#AppURL}

; ── Wizard UI ────────────────────────────────────────────
;  Replace these with your own 164x314 / 150x50 BMPs
;WizardSmallImageFile=assets\wizard_small.bmp
;WizardImageFile=assets\wizard_large.bmp

; ── Misc ──────────────────────────────────────────────────
MinVersion=10.0
DisableProgramGroupPage=auto
DisableWelcomePage=no
CloseApplications=force
RestartApplications=False

; ── License (optional) ───────────────────────────────────
;LicenseFile=LICENSE.txt


[Languages]
Name: "english";    MessagesFile: "compiler:Default.isl"
Name: "spanish";     MessagesFile: "compiler:Languages\Spanish.isl"


[Tasks]
; ── Desktop shortcut ─────────────────────────────────────
Name: "desktopicon";     Description: "{cm:CreateDesktopIcon}";     GroupDescription: "{cm:AdditionalIcons}"; Flags: checked
; ── Quick Launch shortcut ────────────────────────────────
Name: "quicklaunchicon"; Description: "Quick Launch shortcut";       GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
; ── Start at Windows startup ─────────────────────────────
Name: "startupicon";    Description: "Run {#AppName} when Windows starts"; GroupDescription: "Startup:"; Flags: unchecked


[Files]
; ── Main executable (PyInstaller onefile output) ─────────
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; ── README (placed in install folder) ────────────────────
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion


[Icons]
; ── Start Menu Program Group ─────────────────────────────
Name: "{group}\{#AppName}";           Filename: "{app}\{#AppExeName}"; Comment: "Launch {#AppName}"; IconFilename: "{app}\{#AppExeName}"
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"; Comment: "Uninstall {#AppName}"

; ── Desktop shortcut ──────────────────────────────────────
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon; Comment: "Launch {#AppName}"

; ── Quick Launch shortcut ────────────────────────────────
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: quicklaunchicon

; ── Startup shortcut ─────────────────────────────────────
Name: "{userstartup}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: startupicon


[Run]
; ── Launch after install ──────────────────────────────────
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent


[UninstallRun]
; ── Kill launcher if running before uninstall ─────────────
Filename: "taskkill"; Parameters: "/f /im "{#AppExeName}""; Flags: runhidden


[UninstallDelete]
; ── Clean up AppData config ───────────────────────────────
Type: filesandordirs; Name: "{userappdata}\ZenoxGD"
; ── Clean up install directory ───────────────────────────
Type: filesandordirs; Name: "{app}"


[Registry]
; ── Optional: Add to PATH (so you can run from terminal) ──
; Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
;   ValueType: expandsz; ValueName: "Path"; ValueData: "{code:GetExistingPATH};{app}"; \
;   Flags: preservestringtype


[Code]
[Code]
// ── Custom code: Check if already installed and offer to uninstall ──
function InitializeSetup(): Boolean;
var
  OldVersion: String;
  UninstallString: String;
  ResultCode: Integer; // <-- ¡ESTO ES LO QUE FALTABA DECLARAR!
begin
  // Check if previous version exists in registry
  if RegQueryStringValue(HKLM,
    'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}_is1',
    'UninstallString', UninstallString) then
  begin
    if MsgBox('A previous version of {#AppName} is already installed.' #13#10 #13#10 +
              'Do you want to uninstall it first?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      UninstallString := RemoveQuotes(UninstallString);
      Exec(UninstallString, '/SILENT /NORESTART', '', SW_SHOW, ewWaitUntilTerminated, ResultCode);
    end;
  end;
  Result := True;
end;
