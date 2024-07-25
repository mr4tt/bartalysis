import React from 'react';
import { describe, it, expect } from 'vitest';
import { findStation, stationList } from '../src/utils/stations'

describe("stations.ts file", () => {
    const fremontStation = stationList[20]
    const result = findStation("FRMT")

    it("findStation functions works", () => {
        expect(fremontStation).toEqual(result)
    })

    it("object has correct properties and value types", () => {
        expect(fremontStation).toHaveProperty("name")
        expect(fremontStation).toHaveProperty("abbr")
        expect(fremontStation).toHaveProperty("lat")
        expect(fremontStation).toHaveProperty("lng")
        expect(fremontStation).toHaveProperty("address")
        expect(fremontStation).toHaveProperty("city")
        expect(fremontStation).toHaveProperty("county")
        expect(fremontStation).toHaveProperty("state")
        expect(fremontStation).toHaveProperty("zipcode")
    })

    it("lat and lng property are floats after converting from string", () => {
        expect(parseFloat(fremontStation.lat)).not.toBe(Math.floor(parseFloat(fremontStation.lat)))
    })
})