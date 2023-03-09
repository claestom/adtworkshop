# *Set up environment*

## First set variables below

location="westeurope" 

resourceGroup="<insert name>"

storageAccount="<insert name>"

functionApp="<insert name>"

dtName="<insert name>"

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

## Create models

az dt model create --dt-name walloniadt --models location_model.json

az dt model create --dt-name walloniadt --models building_model.json

az dt model create --dt-name walloniadt --models hal_model.json 

az dt model create --dt-name walloniadt --models computer_model.json

az dt model create --dt-name walloniadt --models person_model.json

## Create twins

az dt twin create  --dt-name walloniadt --dtmi "dtmi:contosocom:DigitalTwins:Location;1" --twin-id Charleroi --properties "{\"Latitude\": 50.41, \"Longitude\": 4.44}"

az dt twin create  --dt-name walloniadt --dtmi "dtmi:contosocom:DigitalTwins:Building;1" --twin-id E6KA6K

az dt twin create  --dt-name walloniadt --dtmi "dtmi:contosocom:DigitalTwins:Hal;1" --twin-id Hal1 --properties "{\"nPeople\": 143, \"Humidity\": 56,\"Temperature\":21}"

az dt twin create  --dt-name walloniadt --dtmi "dtmi:contosocom:DigitalTwins:Computer;1" --twin-id SurfaceStudio --properties "{\"CPU\": 23, \"Memory\": 56}"   

az dt twin create  --dt-name walloniadt --dtmi "dtmi:contosocom:DigitalTwins:Person;1" --twin-id Tom

## Create relationships

az dt twin relationship create -n walloniadt --relationship-id rel1 --relationship contains --twin-id Charleroi --target E6KA6K

az dt twin relationship create -n walloniadt --relationship-id rel1 --relationship contains --twin-id E6KA6K --target Hal1    

az dt twin relationship create -n walloniadt --relationship-id rel1 --relationship provides --twin-id Hal1 --target SurfaceStudio

az dt twin relationship create -n walloniadt --relationship-id rel1 --relationship owns --twin-id Tom --target SurfaceStudio

