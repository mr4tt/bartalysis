import { render, screen, } from '@testing-library/react';
import IncomingTrainsContainer from "../src/components/IncomingTrainsContainer"
import React from 'react';
import { describe, it, expect, beforeEach } from 'vitest';
import "@testing-library/jest-dom"

describe("IncomingTrainsContainer.tsx", () => {
    const train = {
        "ArrivalTime": "16:24:00",
        "DepartureTime": "16:15:00",
        "EndingID": "EMBR",
        "StartingID": "24TH",
        "TrainColor": "0099CC",
        "TrainDescription": "Daly City to Dublin/Pleasanton",
        "TrainName": "Blue-N"
    }
    
    beforeEach(() => {
        render(<IncomingTrainsContainer train={train} />);
    });

    it("should contain TrainName property", () => {
        expect(screen.getByText("Train color: " + train.TrainName.slice(0, train.TrainName.length - 2))).toBeInTheDocument()
    })

    it("should contain TrainDescription property", () => {
        expect(screen.getByText(train.TrainDescription)).toBeInTheDocument()
    })

    it("should contain ArrivalTime property", () => {
        expect(screen.getByText(train.ArrivalTime)).toBeInTheDocument()
    })

    it("should contain DepartureTime property", () => {
        expect(screen.getByText(train.DepartureTime)).toBeInTheDocument()
    })
})