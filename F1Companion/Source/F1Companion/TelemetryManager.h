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

USTRUCT(BlueprintType)
struct FRadioData {
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "Radio")
	FString Radio_URL = TEXT("");

	UPROPERTY(BlueprintReadOnly, Category = "Radio")
	FString Timestamp = TEXT("");
};

USTRUCT(BlueprintType)
struct FLocationData {
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "Location")
	float X_coor = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Location")
	float Y_coor = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Location")
	float YAW = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Location")
	float Z_coor = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Location")
	FString Timestamp = TEXT("");
};

USTRUCT(BlueprintType)
struct FIntervalData {
	GENERATED_BODY()
	
	UPROPERTY(BlueprintReadOnly, Category = "Interval")
	float Leader_gap = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Interval")
	float Interval = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Interval")
	FString Timestamp = TEXT("");
};

USTRUCT(BlueprintType)
struct FLapData {
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "Lap")
	int32 LapNumber = 0;

	UPROPERTY(BlueprintReadOnly, Category = "Lap")
	FString Sec1 = TEXT("");

	UPROPERTY(BlueprintReadOnly, Category = "Lap")
	FString Sec2 = TEXT("");

	UPROPERTY(BlueprintReadOnly, Category = "Lap")
	FString Sec3 = TEXT("");

	UPROPERTY(BlueprintReadOnly, Category = "Lap")
	float LapDuration = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Lap")
	bool IsPersonalBest = false;

	UPROPERTY(BlueprintReadOnly, Category = "Lap")
	FString Timestamp = TEXT("");
};
	
USTRUCT(BlueprintType)
struct FRaceControlData{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "Race_Control")
	FString Category = TEXT("");

	UPROPERTY(BlueprintReadOnly, Category = "Race_Control")
	FString Flag = TEXT("");

	UPROPERTY(BlueprintReadOnly, Category = "Race_Control")
	FString Message = TEXT("");

	UPROPERTY(BlueprintReadOnly, Category = "Race_Control")
	FString Timestamp = TEXT("");
};

USTRUCT(BlueprintType)
struct FLeaderboardData {
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "Leaderboard")
	int32 Driver_Number;

	UPROPERTY(BlueprintReadOnly, Category = "Leaderboard")
	int32 Position;

	UPROPERTY(BlueprintReadOnly, Category = "Leaderboard")
	FString Timestamp = TEXT("");
};

USTRUCT(BlueprintType)
struct FSessionInfoData {
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "Session")
	FString Circuit = TEXT("");

	UPROPERTY(BlueprintReadOnly, Category = "Session")
	FString Country = TEXT("");

	UPROPERTY(BlueprintReadOnly, Category = "Session")
	FString Session = TEXT("");

	UPROPERTY(BlueprintReadOnly, Category = "Session")
	FString SessionType = TEXT("");
};

USTRUCT(BlueprintType)
struct FDriverDetails {
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "Driver")
	FString FullName = TEXT("");

	UPROPERTY(BlueprintReadOnly, Category = "Driver")
	FString NameAcronym = TEXT("");

	UPROPERTY(BlueprintReadOnly, Category = "Driver")
	FString TeamColour = TEXT("");
};

USTRUCT(BlueprintType)
struct FStintDetails {
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "Stint")
	FString Compound = TEXT("");

	UPROPERTY(BlueprintReadOnly, Category = "Stint")
	FString TyreDuration = TEXT(""); // FString per supportare sia il numero che il testo "Fino a fine gara"

	UPROPERTY(BlueprintReadOnly, Category = "Stint")
	int32 TyreAgeAtStart = 0;
};

UCLASS()
class F1COMPANION_API UTelemetryManager : public UGameInstance
{
	GENERATED_BODY()
public:
	virtual void Init() override;
	virtual void Shutdown() override;

	// Oggetti per funzioni di setup
	UPROPERTY(BlueprintReadOnly, Category = "Setup")
	FSessionInfoData CurrentSessionInfo;

	UPROPERTY(BlueprintReadOnly, Category = "Setup")
	TMap<int32, FDriverDetails> DriversRegistry;

	UPROPERTY(BlueprintReadOnly, Category = "Setup")
	TMap<int32, FStintDetails> StintsRegistry;


	// Oggetti per funzioni live
	UPROPERTY(BlueprintReadOnly, Category = "Telemetry")
	FVehicleTelemetryData CurrentTelemetry; // Oggetto telemtria corrente

	UPROPERTY(BlueprintReadOnly, Category = "Weather")
	FWeatherData CurrentWeather;

	UPROPERTY(BlueprintReadOnly, Category = "Radio")
	FRadioData CurrentRadio;

	UPROPERTY(BlueprintReadOnly, Category = "Location")
	FLocationData CurrentLocation;

	UPROPERTY(BlueprintReadOnly, Category = "Interval")
	FIntervalData CurrentInterval;

	UPROPERTY(BlueprintReadOnly, Category = "Lap")
	FLapData CurrentLap;

	UPROPERTY(BlueprintReadOnly, Category = "Race_Control")
	FRaceControlData CurrentControlData;

	UPROPERTY(BlueprintReadOnly, Category = "Leaderboard")
	FLeaderboardData CurrentLeaderboard;

private:
	FSocket* ReceiverSocket;	// Puntatore al ricevitore UDP
	FTimerHandle UDPReceiveTimerHandle; // Cronometro interno di Unreal Engine per gestire la ricezione dei pacchetti UDP

	void ReceiveUDPData();	// Riceve i pacchetti UDP, legge i byte in arrivo e li traduce in stringhe
	void RoutePacket(const TSharedPtr<FJsonObject>& JsonObject); // Instrada i pacchetti in base al loro tipo verso l'handler corretto

	void HandleDashboardData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleWeatherData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleRadioCommsData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleLocationData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleIntervalsData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleLapsData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleRaceControlData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleLeaderboardData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleSessionInfoData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleDriverInfoData(const TSharedPtr<FJsonObject>& DataObject);
	void HandleStintsInfoData(const TSharedPtr<FJsonObject>& DataObject);
	
};
