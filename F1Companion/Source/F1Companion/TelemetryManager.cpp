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
			const TSharedPtr<FJsonObject>* DataObjectPtr;
			if (JsonObject->TryGetObjectField(TEXT("data"), DataObjectPtr))
			{
				TSharedPtr<FJsonObject> DataObject = *DataObjectPtr;

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
		}

		if (GEngine)
		{
			GEngine->AddOnScreenDebugMessage(-1, 5.f, FColor::Green, FString::Printf(TEXT("Python dice: %s"), *ReceivedString));
		}
	}
}