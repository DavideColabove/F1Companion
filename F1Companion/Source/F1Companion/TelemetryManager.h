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

USTRUCT(BlueprintType)
struct FWeatherData {
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "Weather")
	float Air_Temp = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Weather")
	float Track_Temp = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Weather")
	float Humidity = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Weather")
	float Rainfall = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Weather")
	FString Timestamp = TEXT("");

	UPROPERTY(BlueprintReadOnly, Category = "Weather")
	float Wind_Speed = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Weather")
	float Wind_Direction = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Weather")
	float Pressure = 0.0f;

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

	UPROPERTY(BlueprintReadOnly, Category = "Weather")
	FWeatherData CurrentWeather;
private:
	FSocket* ReceiverSocket;	// Puntatore al ricevitore UDP
	FTimerHandle UDPReceiveTimerHandle; // Cronometro interno di Unreal Engine per gestire la ricezione dei pacchetti UDP

	void ReceiveUDPData();	// Funzione per ricevere i pacchetti UDP, leggere i byte in arrivo e tradurli in stringhe
	void RoutePacket(const TSharedPtr<FJsonObject>& JsonObject);

	void HandleDashboardData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleWeatherData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleRadioCommsData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleLocationData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleIntervalsData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleLapsData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleRaceControlData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleLeaderboardData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleSessionInfoData(const TSharedPtr<FJsonObject>& DataObject);
	
};
