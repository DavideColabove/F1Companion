// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Engine/GameInstance.h"
#include "Networking.h"
#include "Sockets.h"
#include "TelemetryManager.generated.h"

/**
 * 
 */
UCLASS()
class F1COMPANION_API UTelemetryManager : public UGameInstance
{
	GENERATED_BODY()
public:
	virtual void Init() override;
	virtual void Shutdown() override;
private:
	FSocket* RecieverSocket;	// Puntatore al ricevitore UDP
	FTimerHandle UDPReceiveTimerHandle; // Cronometro interno di Unreal Engine per gestire la ricezione dei pacchetti UDP

	void ReceiveUDPData();	// Funzione per ricevere i pacchetti UDP, leggere i byte in arrivo e tradurli in stringhe
	
};
