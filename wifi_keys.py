import subprocess
import re
import wifi

wifi_names = 'netsh wlan show profiles'
result = subprocess.run(wifi_names, capture_output=True, text=True)

profiles = result.stdout

profile_names = re.findall(r':\s+(.*)', profiles)
orginal_names = profile_names[1:]

if orginal_names:
    for name in orginal_names:
       
        keys_result = subprocess.run(f"{wifi_names} name=\"{name}\" key=clear", capture_output=True, text=True)
        keys_output = keys_result.stdout
        
        key_content = re.search(r'Key Content\s+:\s(.*)', keys_output)
        
        if key_content:
            print(f"{name}: {key_content.group(1)}")
        else:
            print(f"{name}: key not found.")
else:
    print("No WiFi networks found.")
