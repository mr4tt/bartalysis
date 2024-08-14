import React from 'react';
import { describe, it, expect, beforeEach } from 'vitest';
import { getNextThreeTrains, countDecimals, sortFares, formatTime } from "../src/utils/utils"

describe("utils.js", async() => {
    const now = new Date().toTimeString().slice(0,9)
    const nextThreeTrains = await fetchData()
    let flag = true

    it("tests getNextTreeTrains function", () => {
    it("tests getNextTreeTrains function", () => {
        for (let i = 0; i < nextThreeTrains.length; i++) {
            if (nextThreeTrains[i].ArrivalTime < now) {
            if (nextThreeTrains[i].ArrivalTime < now) {
                flag = false
                return
            }
        }
        expect(flag).toBe(true);
    })

    it("tests countDecimals function", () => {
        expect(countDecimals(10)).toBe(0)
        expect(countDecimals(10.0)).toBe(0)
        expect(countDecimals(10.1)).toBe(1)
        expect(countDecimals(10.11)).toBe(2)
        expect(countDecimals(10.101)).toBe(3)
    })

    it ("should correctly sort using sortFares() based on the Price property", () => {
        const fare1 = {"Description": "", "FareID": 1, "Price": 1}
        const fare3 = {"Description": "", "FareID": 3, "Price": 3}
        const fare2 = {"Description": "", "FareID": 2, "Price": 2}
        const fares = [fare3, fare2, fare1]
        const expectedResult = [fare1, fare2, fare3]
        expect(sortFares(fares)).toEqual(expectedResult)
        expect(sortFares(fares).length).toBe(3)
    })

    it("should return an array with length of 0", () => {
        expect(sortFares([]).length).toBe(0)
    })

    it("should return an array with length of 1", () => {
        expect(sortFares([{"Description": "", "FareID": 1, "Price": 1}])).toEqual([{"Description": "", "FareID": 1, "Price": 1}])
        expect(sortFares([{"Description": "", "FareID": 1, "Price": 1}]).length).toBe(1)
    })

    it("should output the correct time format", () => {
        const time1 = "01:59:00"
        const time2 = "09:59:00"
        const time3 = "10:00:00"
        const time4 = "12:00:00"
        const time5 = "13:00:00"
        expect(formatTime(time1)).toBe("1:59 am")
        expect(formatTime(time2)).toBe("9:59 am")
        expect(formatTime(time3)).toBe("10:00 am")
        expect(formatTime(time4)).toBe("12:00 pm")
        expect(formatTime(time5)).toBe("1:00 pm")

    })
})

const fetchData = async() => {
    const response = await fetch('https://bug-free-space-meme-956jrx6xpjx29xr4-8000.app.github.dev/route-planner/DALY/SHAY/?date=2024-08-15&time=08:00:00')
    const data = await response.json()
    const nextThreeTrains = getNextThreeTrains(data.trains)
   return nextThreeTrains
}
