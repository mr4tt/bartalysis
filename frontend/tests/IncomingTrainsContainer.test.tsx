import { render, screen, } from '@testing-library/react';
import IncomingTrainsContainer from "../src/components/IncomingTrainsContainer"
import React from 'react';
import { describe, it, expect } from 'vitest';
import "@testing-library/jest-dom/vitest"

describe("IncomingTrainsContainer component", () => {
    // TrainName, TrainDescript, ArrivalTime, DepartureTime
    const train = {
        "ArrivalTime": "16:24:00",
        "DepartureTime": "16:15:00",
        "EndingID": "EMBR",
        "StartingID": "24TH",
        "TrainColor": "0099CC",
        "TrainDescription": "Daly City to Dublin/Pleasanton",
        "TrainName": "Blue-N"
    }
    render(<IncomingTrainsContainer train={train}/>)

    it("should contain TrainName", () => {
        expect(screen.getByText("Train color: " + train.TrainName.slice(0, train.TrainName.length - 2))).toBeInTheDocument()
    })

    // it("should contain DepartureTime", () => {
    //     expect(screen.getByText("Incoming at: " + train.DepartureTime)).toBeInTheDocument()
    // })
})