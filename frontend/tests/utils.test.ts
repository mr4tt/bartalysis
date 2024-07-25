import React from 'react';
import { describe, it, expect, beforeEach } from 'vitest';
import { getNextThreeTrains } from "../src/utils/utils"

describe("utils.js", async() => {
    const now = new Date().toTimeString().slice(0,9)
    const nextThreeTrains = await fetchData()
    let flag = true

    it("test getNextTreeTrains function", () => {
        for (let i = 0; i < nextThreeTrains.length; i++) {
            if (nextThreeTrains[i].arrivalTime < now) {
                flag = false
                return
            }
        }
    })
    expect(flag).toBe(true)
})

const fetchData = async() => {
    const response = await fetch('https://bug-free-space-meme-956jrx6xpjx29xr4-8000.app.github.dev/route-planner/DALY/SHAY/?date=2024-08-13&time=08:00:00')
    const data = await response.json()
    const nextThreeTrains = getNextThreeTrains(data.trains)
   return nextThreeTrains
}
