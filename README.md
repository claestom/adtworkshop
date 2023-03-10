# *Set up environment*
## First set variables below

location="westeurope" 

resourceGroup=rghackathon$(shuf -i 10000-99999 -n 1)

storageAccount=sahackathon$(shuf -i 10000-99999 -n 1)

functionApp=fahackathon$(shuf -i 10000-99999 -n 1)

dtName=dthackathon$(shuf -i 10000-99999 -n 1)

iotHubName=iothubhackathon$(shuf -i 10000-99999 -n 1)

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

