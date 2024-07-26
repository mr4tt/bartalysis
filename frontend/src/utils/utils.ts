import { train } from "./types"

export const getNextThreeTrains = (trains: train[]) => {
    let counter = 0
    let flag = false
    const now = new Date().toTimeString().slice(0,9)
    const nextThreeTrains = trains.filter((train: train) => {
        if (train.DepartureTime >= now) flag = true
        if (!flag || counter >= 3) return
        counter++
        return train.DepartureTime >= now
    })
    return nextThreeTrains
}

export const countDecimals = (val: number) => {
    if (Math.floor(val) === val) return 0;
    return val.toString().split(".")[1].length || 0; 
}