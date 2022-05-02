import subprocess
import argparse

parser = argparse.ArgumentParser(description='Python app to generate FirewallD Service Files')
parser.add_argument('--Generic', action="store_true", dest="generic", default=False, help="Generates IRIS Service File for Mirroring and Licensing ports")
parser.add_argument('--All-Instances', action="store_true", dest="AllInstances", default=False, help="Generates Service Files for all Intsances on this server")
parser.add_argument('--Instance', action="store", dest="Instance", default=False, help="Generates Service Files for Intsance specified")

a = parser.parse_args()

def createGenericServiceFiles():
    serviceFileContents = f"""<?xml version=\"1.0\" encoding=\"utf-8\"?>
    <service>
    <short>IRIS</short>
    <description>IRIS Ports for Mirroring (2188) and Licensing (4001)</description>
    <port port="2188" protocol="tcp"/>
    <port port="4001" protocol="tcp"/>
</service>"""
    try:
        fileName = f"IRIS.xml"
        with open(fileName, 'w') as f:
            f.write(serviceFileContents)
    except: 
        print(f"Failed to save services file: {fileName}")
    else:
        print(f"{f.name} Written, Use the bellow commands to activate")
        print(f"\tsudo firewall-cmd --permanent --new-service-from-file={f.name} --name=IRIS")
        print(f"\tsudo firewall-cmd --permanent --add-service=IRIS")




def createInstanceServiceFiles():
    p = subprocess.Popen(["iris","qlist"], stdout=subprocess.PIPE)
    qlist = p.communicate()

    for i in qlist[0].decode('utf-8').split('\n'): 
        if i != '':
            serviceFileContents = f"""<?xml version=\"1.0\" encoding=\"utf-8\"?>
        <service>
        <short>{i.split('^')[0]}</short>
        <description>{i.split('^')[0]} superserver ({i.split('^')[5]}) and webserver ({i.split('^')[6]}) ports</description>
        <port port="{i.split('^')[5]}" protocol="tcp"/>
        <port port="{i.split('^')[6]}" protocol="tcp"/>
    </service>"""

            try:
                fileName = f"{i.split('^')[0]}.xml"
                with open(fileName, 'w') as f:
                    f.write(serviceFileContents)
            except: 
                print("Failed to save services file")
            else:
                print(f"{f.name} Written, Use the bellow commands to activate")
                print(f"\tsudo firewall-cmd --permanent --new-service-from-file={f.name} --name={i.split('^')[0]}")
                print(f"\tsudo firewall-cmd --permanent --add-service={i.split('^')[0]}")

def createInstanceServiceFileByName(InstanceName):
    p = subprocess.Popen(["iris","qlist"], stdout=subprocess.PIPE)
    qlist = p.communicate()

    for i in qlist[0].decode('utf-8').split('\n'): 
        if i.split('^')[0] == InstanceName:
            serviceFileContents = f"""<?xml version=\"1.0\" encoding=\"utf-8\"?>
        <service>
        <short>{i.split('^')[0]}</short>
        <description>{i.split('^')[0]} superserver ({i.split('^')[5]}) and webserver ({i.split('^')[6]}) ports</description>
        <port port="{i.split('^')[5]}" protocol="tcp"/>
        <port port="{i.split('^')[6]}" protocol="tcp"/>
    </service>"""

            try:
                fileName = f"{i.split('^')[0]}.xml"
                with open(fileName, 'w') as f:
                    f.write(serviceFileContents)
            except: 
                print("Failed to save services file")
            else:
                print(f"{f.name} Written, Use the bellow commands to activate")
                print(f"\tsudo firewall-cmd --permanent --new-service-from-file={f.name} --name={i.split('^')[0]}")
                print(f"\tsudo firewall-cmd --permanent --add-service={i.split('^')[0]}")


if a.generic:
    createGenericServiceFiles()
if a.AllInstances:
    createInstanceServiceFiles()
if a.Instance:
    createInstanceServiceFileByName(a.Instance)