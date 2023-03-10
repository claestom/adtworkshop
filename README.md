# STEP 1: Set up environment

## Download required tools

Download VS Code: https://code.visualstudio.com/download

Download .NET 6.0: https://dotnet.microsoft.com/en-us/download

Go to the Azure Portal and create account:

- Students: [Azure for Students](https://azure.microsoft.com/en-us/free/students/)
    
- Non-students: [Free Azure Trial](https://azure.microsoft.com/en-gb/free/search/?OCID=AIDcmm3bvqzxp1_SEM_a12a261aff841e1a17f24211a7299a56:G:s&ef_id=a12a261aff841e1a17f24211a7299a56:G:s&msclkid=a12a261aff841e1a17f24211a7299a56)

## First set variables below

Open the Azure Portal and start a [bash session](https://learn.microsoft.com/en-us/azure/cloud-shell/quickstart?tabs=azurecli)

    location="westeurope" 

    resourceGroup=rghackathon$(shuf -i 10000-99999 -n 1)

    storageAccount=sahackathon$(shuf -i 10000-99999 -n 1)

    functionApp=fahackathon$(shuf -i 10000-99999 -n 1)

    dtName=dthackathon$(shuf -i 10000-99999 -n 1)

    iotHubName=iothubhackathon$(shuf -i 10000-99999 -n 1)

    deviceName=device$(shuf -i 10000-99999 -n 1)

    eventhubSub=ehsub$(shuf -i 10000-99999 -n 1)

## Copy paste commands below in bash session

    az extension add --name functionapp

    az extension add --name azure-iot

    az extension update --name azure-iot

    az group create --name $resourceGroup --location $location

    az iot hub create --name $iotHubName --resource-group $resourceGroup --sku S1 

    az storage account create --name $storageAccount --resource-group $resourceGroup --location $location --sku Standard_LRS --kind StorageV2

    key=$(az storage account keys list -g $resourceGroup -n $storageAccount --query "[0].value" -o tsv)

    az storage container create --account-name $storageAccount --name container1 --account-key $key

    az functionapp create --resource-group $resourceGroup --consumption-plan-location $location --runtime dotnet --functions-version 4 --name $functionApp --storage-account $storageAccount

    az dt create --dt-name $dtName --resource-group $resourceGroup --location $location 

## Assign Data Owner role to your user

    az ad signed-in-user show

### *Copy the 'id' value and replace the "id-value" in the next command with "id", don't forget to put it between " "*

    az dt role-assignment create --dt-name $dtName --assignee "id-value" --role "Azure Digital Twins Data Owner"

## Create models

    git clone https://github.com/claestom/adtworkshop.git
    
    cd adtworkshop

    az dt model create --dt-name $dtName --models location_model.json

    az dt model create --dt-name $dtName --models building_model.json

    az dt model create --dt-name $dtName --models hal_model.json 

    az dt model create --dt-name $dtName --models computer_model.json

    az dt model create --dt-name $dtName --models person_model.json

## Create twins

    az dt twin create  --dt-name $dtName --dtmi "dtmi:contosocom:DigitalTwins:Location;1" --twin-id Charleroi --properties '{\"Latitude\": 50.41, \"Longitude\": 4.44}'

    az dt twin create  --dt-name $dtName --dtmi "dtmi:contosocom:DigitalTwins:Building;1" --twin-id E6KA6K

    az dt twin create  --dt-name $dtName --dtmi "dtmi:contosocom:DigitalTwins:Hal;1" --twin-id Hal1 --properties '{\"nPeople\": 143, \"Humidity\": 56,\"Temperature\":21}'

    az dt twin create  --dt-name $dtName --dtmi "dtmi:contosocom:DigitalTwins:Computer;1" --twin-id SurfaceStudio --properties '{\"CPU\": 23, \"Memory\": 56}'  

    az dt twin create  --dt-name $dtName --dtmi "dtmi:contosocom:DigitalTwins:Person;1" --twin-id Tom

## Create relationships

    az dt twin relationship create -n $dtName --relationship-id rel1 --relationship contains --twin-id Charleroi --target E6KA6K

    az dt twin relationship create -n $dtName --relationship-id rel1 --relationship contains --twin-id E6KA6K --target Hal1    

    az dt twin relationship create -n $dtName --relationship-id rel1 --relationship provides --twin-id Hal1 --target SurfaceStudio

    az dt twin relationship create -n $dtName --relationship-id rel1 --relationship owns --twin-id Tom --target SurfaceStudio

# STEP 2: Configure IoT Hub and Azure Functions
## Create device in IoT Hub to connect to

    az iot hub device-identity create --hub-name $iotHubName --device-id $deviceName

    az iot hub device-identity connection-string show --hub-name $iotHubName --device-id $deviceName

--> Copy the 'connectionString'

    vim iotdevice.py

    i

--> Paste the replace connectionString with the value you just copied and press 'esc' afterwards

    :wq

--> You should have returned to the original window

    /usr/bin/python3.9 -m pip install --upgrade pip

    pip install azure-iot-hub azure-iot-device

    python iotdevice.py

# STEP 3: Create and deploy Azure Functions

## Open local command prompt

    mkdir digitaltwin

    cd digitaltwin

    code .

### First install following extensions:

    Ctrl + shift + X

    Azure Tools

    Azure Account

### Sign in to Azure and create Function

Ctrl + shift + P

Search: Azure: Sign In 

    Shift + Alt + A

Go to *Workspace* and click on *Create Function...* 

On top a pop-up will follow.

    Select *digitaltwin*

    C#

    .NET LTS

    Azure Event Grid trigger

    Replace EventGridTrigger1 with digitaltwindemo

    Leave namespace like it is (enter)

    Ctrl + Shift + E

open *digitaltwindemo.cs*

### Download following packages by running the commands below in a terminal window inside VS Code

Open new terminal: Ctrl + SHift + ù

    dotnet add package Azure.DigitalTwins.Core --version 1.4.0

    dotnet add package Azure.Identity --version 1.8.2

    dotnet add package Microsoft.Azure.WebJobs.Extensions.EventGrid --version 3.2.1

### Add code to Function and deploy to the cloud

    Ctrl + Shift + E

Replace code with code inside *functioncode.py* (GitHub - https://github.com/claestom/adtworkshop/blob/main/functioncode.py)

    Shift + Alt + A

Go to *Workspace* and click *Deploy...* and next *Deploy to Function App...*

    Pop-up will follow on top

    Select

    Select Subscription

    Select functionapp created

    Wait until deployment is completed (~1 minute)

### Configure settings of the Function and connect to the IoT Hub

    az functionapp identity assign --resource-group $resourceGroup --name $functionApp

    --> Copy the PrincipalId and past it between " " as the principal-ID in the command below

    az dt role-assignment create --dt-name $dtName --assignee "" --role "Azure Digital Twins Data Owner"

    az dt show --dt-name $dtName

    --> Copy the hostname and past it after *https://*

    az functionapp config appsettings set --resource-group $resourceGroup --name $functionApp --settings "ADT_SERVICE_URL=https://"

    subId=$(az account show --query 'id' --output tsv)

    az provider register --namespace Microsoft.Web

    az provider register --namespace Microsoft.EventGrid

    az eventgrid event-subscription create --name $eventhubSub --event-delivery-schema eventgridschema --source-resource-id /subscriptions/$subId/resourceGroups/$resourceGroup/providers/Microsoft.Devices/IotHubs/$iotHubName --included-event-types Microsoft.Devices.DeviceTelemetry --endpoint-type azurefunction --endpoint /subscriptions/$subId/resourceGroups/$resourceGroup/providers/Microsoft.Web/sites/$functionApp/functions/IoTHubtoTwins

# STEP 4: Test E2E solution

    python iotdevice.py
    
Go to your Azure Digital Twins instance in the Azure Portal and open the *Azure Digital Twins Explorer (preview)*
