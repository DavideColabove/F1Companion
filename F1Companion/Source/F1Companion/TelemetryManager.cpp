#include "TelemetryManager.h"
#include "Common/UdpSocketBuilder.h"
#include "TimerManager.h"            
#include "Engine/World.h"      
#include "SocketSubsystem.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

void UTelemetryManager::Init()
{
	Super::Init();

	// Crea il socket
	ReceiverSocket = FUdpSocketBuilder(TEXT("F1TelemetrySocket")).AsNonBlocking().AsReusable().BoundToAddress(FIPv4Address(127, 0, 0, 1)).BoundToPort(5555).Build();

	// Avvia il timer
	GetWorld()->GetTimerManager().SetTimer(UDPReceiveTimerHandle, this, &UTelemetryManager::ReceiveUDPData, 0.016f, true);
	
}

void UTelemetryManager::Shutdown()
{
	if(GetWorld()) // Fermo il timer
		GetWorld()->GetTimerManager().ClearTimer(UDPReceiveTimerHandle); 
	if (ReceiverSocket != nullptr) { // Libero la memoria del socket
		ReceiverSocket->Close();
		ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(ReceiverSocket);
	}
	Super::Shutdown();
}

void UTelemetryManager::ReceiveUDPData()
{
	if (!ReceiverSocket)
		return;

	uint32 size;
	while (ReceiverSocket->HasPendingData(size)) {
		TArray<uint8> ReceivedData;
		ReceivedData.Init(0, FMath::Min(size, 65507u));
		int32 BytesRead = 0;
		ReceiverSocket->Recv(ReceivedData.GetData(), ReceivedData.Num(), BytesRead);

		ReceivedData.Add(0); // Terminatore
		FString ReceivedString = UTF8_TO_TCHAR(ReceivedData.GetData());

		TSharedPtr<FJsonObject> JsonObject;
		TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(ReceivedString);

		if (FJsonSerializer::Deserialize(Reader, JsonObject) && JsonObject.IsValid())
		{
			RoutePacket(JsonObject);
		}

		if (GEngine)
		{
			GEngine->AddOnScreenDebugMessage(-1, 5.f, FColor::Green, FString::Printf(TEXT("Python dice: %s"), *ReceivedString));
		}
	}
}

void UTelemetryManager::RoutePacket(const TSharedPtr<FJsonObject>& JsonObject)
{
	FString PacketId;
	if (!JsonObject->TryGetStringField(TEXT("packet_id"), PacketId))
	{
		return;
	}

	const TSharedPtr<FJsonObject>* DataObjectPtr;
	if (JsonObject->TryGetObjectField(TEXT("data"), DataObjectPtr))
	{
		TSharedPtr<FJsonObject> DataObject = *DataObjectPtr;

		if (PacketId == TEXT("dashboard_data"))
		{
			HandleDashboardData(DataObject);
		}
		else if (PacketId == TEXT("weather_data"))
		{
			HandleWeatherData(DataObject);
		}
		else if (PacketId == TEXT("radio_comms_data"))
		{
			HandleRadioCommsData(DataObject);
		}
		else if (PacketId == TEXT("location_data"))
		{
			HandleLocationData(DataObject);
		}
		else if (PacketId == TEXT("intervals_data"))
		{
			HandleIntervalsData(DataObject);
		}
		/*else if (PacketId == TEXT("laps_data"))
		{
			HandleLapsData(DataObject);
		}
		else if (PacketId == TEXT("race_control_data"))
		{
			HandleRaceControlData(DataObject);
		}
		else if (PacketId == TEXT("leaderboard_data"))
		{
			HandleLeaderboardData(DataObject);
		}*/
	}
}

void UTelemetryManager::HandleDashboardData(const TSharedPtr<FJsonObject>& DataObject)
{
	int32 TempGear;
	if (DataObject->TryGetNumberField(TEXT("gear_number"), TempGear))
		CurrentTelemetry.Gear = TempGear;

	int32 TempRPM;
	if (DataObject->TryGetNumberField(TEXT("rpm"), TempRPM))
		CurrentTelemetry.RPM = TempRPM;

	double TempSpeed;
	if (DataObject->TryGetNumberField(TEXT("speed"), TempSpeed))
		CurrentTelemetry.Speed = TempSpeed;

	int32 TempThrottle;
	if (DataObject->TryGetNumberField(TEXT("throttle"), TempThrottle))
		CurrentTelemetry.Throttle = TempThrottle;

	double TempBrake;
	if (DataObject->TryGetNumberField(TEXT("brake"), TempBrake))
		CurrentTelemetry.Brake = TempBrake;

	int32 TempDrs;
	if (DataObject->TryGetNumberField(TEXT("drs"), TempDrs))
		CurrentTelemetry.Drs = TempDrs;

	FString TempTimestamp;
	if (DataObject->TryGetStringField(TEXT("timestamp"), TempTimestamp))
		CurrentTelemetry.Timestamp = TempTimestamp;
}

void UTelemetryManager::HandleWeatherData(const TSharedPtr<FJsonObject>& DataObject) {
	double TempAirTemp;
	if (DataObject->TryGetNumberField((TEXT("air_temp")), TempAirTemp))
		CurrentWeather.Air_Temp = TempAirTemp;

	double TempTrackTemp;
	if (DataObject->TryGetNumberField((TEXT("track_temp")), TempTrackTemp))
		CurrentWeather.Track_Temp = TempTrackTemp;

	double TempHumidity;
	if (DataObject->TryGetNumberField((TEXT("humidity")), TempHumidity))
		CurrentWeather.Humidity = TempHumidity;

	double TempRainfall;
	if (DataObject->TryGetNumberField((TEXT("rainfall")), TempRainfall))
		CurrentWeather.Rainfall = TempRainfall;

	FString TempTimestamp;
	if (DataObject->TryGetStringField(TEXT("timestamp"), TempTimestamp))
		CurrentWeather.Timestamp = TempTimestamp;

	float TempWindSpeed;
	if (DataObject->TryGetNumberField((TEXT("wind_speed")), TempWindSpeed))
		CurrentWeather.Wind_Speed = TempWindSpeed;

	double TempWindDir;
	if (DataObject->TryGetNumberField((TEXT("wind_dir")), TempWindDir))
		CurrentWeather.Wind_Direction = TempWindDir;

	double TempPressure;
	if (DataObject->TryGetNumberField((TEXT("pressure")), TempPressure))
		CurrentWeather.Pressure = TempPressure;
}

void UTelemetryManager::HandleRadioCommsData(const TSharedPtr<FJsonObject>& DataObject){
	FString TempTimestamp;
	if (DataObject->TryGetStringField(TEXT("timestamp"), TempTimestamp))
		CurrentRadio.Timestamp = TempTimestamp;

	FString TempURL;
	if (DataObject->TryGetStringField(TEXT("recording_url"), TempURL))
		CurrentRadio.Radio_URL = TempURL;
}

void UTelemetryManager::HandleLocationData(const TSharedPtr<FJsonObject>& DataObject) {
	double TempX;
	if (DataObject->TryGetNumberField((TEXT("x_coordinate")), TempX))
		CurrentLocation.X_coor = TempX;

	double TempY;
	if (DataObject->TryGetNumberField((TEXT("y_coordinate")), TempY))
		CurrentLocation.Y_coor = TempY;

	double TempYAW;
	if (DataObject->TryGetNumberField((TEXT("yaw")), TempYAW))
		CurrentLocation.YAW = TempYAW;

	double TempZ;
	if (DataObject->TryGetNumberField((TEXT("z_coordinate")), TempZ))
		CurrentLocation.Z_coor = TempZ;

	FString TempTimestamp;
	if (DataObject->TryGetStringField(TEXT("timestamp"), TempTimestamp))
		CurrentLocation.Timestamp = TempTimestamp;
}

void UTelemetryManager::HandleIntervalsData(const TSharedPtr<FJsonObject>& DataObject) {
	double TempLeader_Gap;
	if (DataObject->TryGetNumberField((TEXT("leader_gap")), TempLeader_Gap))
		CurrentInterval.Leader_gap = TempLeader_Gap;

	double TempInterval;
	if (DataObject->TryGetNumberField((TEXT("interval")), TempInterval))
		CurrentInterval.Interval = TempInterval;

	FString TempTimestamp;
	if (DataObject->TryGetStringField(TEXT("timestamp"), TempTimestamp))
		CurrentInterval.Timestamp = TempTimestamp;
}

void UTelemetryManager::HandleLapsData(const TSharedPtr<FJsonObject>& DataObject)
{
	int32 TempLapNumber;
	if (DataObject->TryGetNumberField(TEXT("lap_number"), TempLapNumber))
		CurrentLap.LapNumber = TempLapNumber;

	TSharedPtr<FJsonValue> Sec1Val = DataObject->TryGetField(TEXT("sec1"));
	if (Sec1Val.IsValid())
		CurrentLap.Sec1 = Sec1Val->AsString();

	TSharedPtr<FJsonValue> Sec2Val = DataObject->TryGetField(TEXT("sec2"));
	if (Sec2Val.IsValid())
		CurrentLap.Sec2 = Sec2Val->AsString();

	TSharedPtr<FJsonValue> Sec3Val = DataObject->TryGetField(TEXT("sec3"));
	if (Sec3Val.IsValid())
		CurrentLap.Sec3 = Sec3Val->AsString();

	double TempLapDuration;
	if (DataObject->TryGetNumberField(TEXT("lap_duration"), TempLapDuration))
		CurrentLap.LapDuration = TempLapDuration;

	bool TempIsPB;
	if (DataObject->TryGetBoolField(TEXT("is_personal_best"), TempIsPB))
		CurrentLap.IsPersonalBest = TempIsPB;

	FString TempTimestamp;
	if (DataObject->TryGetStringField(TEXT("timestamp"), TempTimestamp))
		CurrentLap.Timestamp = TempTimestamp;
}