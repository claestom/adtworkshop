using System;
using Azure;
using System.Net.Http;
using Azure.Core.Pipeline;
using Azure.DigitalTwins.Core;
using Azure.Identity;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.EventGrid;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Azure.Messaging.EventGrid;
using System.Text;

namespace Company.Function
{
    public class IoTHubtoTwins
    {
        private static readonly string adtInstanceUrl = Environment.GetEnvironmentVariable("ADT_SERVICE_URL");
        private static readonly HttpClient httpClient = new HttpClient();

        [FunctionName("IoTHubtoTwins")]
        // While async void should generally be used with caution, it's not uncommon for Azure function apps, since the function app isn't awaiting the task.
#pragma warning disable AZF0001 // Suppress async void error
        public async void Run([EventGridTrigger] EventGridEvent eventGridEvent, ILogger log)
#pragma warning restore AZF0001 // Suppress async void error
        {
            if (adtInstanceUrl == null) log.LogError("Application setting \"ADT_SERVICE_URL\" not set");

            try
            {
                // Authenticate with Digital Twins
                var cred = new DefaultAzureCredential();
                var client = new DigitalTwinsClient(new Uri(adtInstanceUrl), cred);
                log.LogInformation($"ADT service client connection created.");
            
                if (eventGridEvent != null && eventGridEvent.Data != null)
                {
                    log.LogInformation(eventGridEvent.Data.ToString());

                    // <Find_device_ID_and_temperature>
                    JObject deviceMessage = (JObject)JsonConvert.DeserializeObject(eventGridEvent.Data.ToString());
                    string deviceId = (string)deviceMessage["systemProperties"]["iothub-connection-device-id"];
                    string encoded_body = (string)deviceMessage["body"];

                    // string body = decode body base 64
                    string decoded_body = Encoding.UTF8.GetString(Convert.FromBase64String(encoded_body));
                    log.LogInformation(decoded_body);

                    JObject body_json = (JObject)JsonConvert.DeserializeObject(decoded_body);
                    var nPeople = body_json["nPeople"];
                    var CPU = body_json["CPU"];
                    var Humidity = body_json["Humidity"];
                    var Memory = body_json["Memory"];
                    var Temperature = body_json["Temperature"];
                    // </Find_device_ID_and_temperature>

                    log.LogInformation($"Number of People is:{nPeople}");

                    // <Update_twin_with_device_temperature>
                    var updateTwinData = new JsonPatchDocument();
                    var updateTwinDataComputer = new JsonPatchDocument();
                    updateTwinData.AppendReplace("/nPeople", nPeople.Value<double>());
                    updateTwinData.AppendReplace("/Humidity", Humidity.Value<double>());
                    updateTwinData.AppendReplace("/Temperature", Temperature.Value<double>());
                    updateTwinDataComputer.AppendReplace("/CPU", CPU.Value<double>());
                    updateTwinDataComputer.AppendReplace("/Memory", Memory.Value<double>());
                    await client.UpdateDigitalTwinAsync(deviceId, updateTwinData);
                    await client.UpdateDigitalTwinAsync("SurfaceStudio", updateTwinDataComputer);
                    // </Update_twin_with_device_temperature>
                }
            }
            catch (Exception ex)
            {
                log.LogError($"Error in ingest function: {ex.Message}");
            }
        }
    }
}