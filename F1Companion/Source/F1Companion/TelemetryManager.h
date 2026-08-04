// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Engine/GameInstance.h"
#include "Networking.h"
#include "Sockets.h"
#include "TelemetryManager.generated.h"

USTRUCT(BlueprintType)
struct FVehicleTelemetryData {
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "Telemetry")
	int32 Gear = 0;

	UPROPERTY(BlueprintReadOnly, Category = "Telemetry")
	float Speed = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Telemetry")
	int32 RPM = 0;

	UPROPERTY(BlueprintReadOnly, Category = "Telemetry")
	int32 Throttle = 0;

	UPROPERTY(BlueprintReadOnly, Category = "Telemetry")
	float Brake = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Telemetry")
	int32 Drs = 0;

	UPROPERTY(BlueprintReadOnly, Category = "Telemetry")
	FString Timestamp = TEXT("");
};

UCLASS()
class F1COMPANION_API UTelemetryManager : public UGameInstance
{
	GENERATED_BODY()
public:
	virtual void Init() override;
	virtual void Shutdown() override;

	UPROPERTY(BlueprintReadOnly, Category = "Telemetry")
	FVehicleTelemetryData CurrentTelemetry; // Oggetto telemtria corrente
private:
	FSocket* ReceiverSocket;	// Puntatore al ricevitore UDP
	FTimerHandle UDPReceiveTimerHandle; // Cronometro interno di Unreal Engine per gestire la ricezione dei pacchetti UDP

	void ReceiveUDPData();	// Funzione per ricevere i pacchetti UDP, leggere i byte in arrivo e tradurli in stringhe
	
};
