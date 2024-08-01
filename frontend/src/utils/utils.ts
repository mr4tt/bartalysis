import { train, fare } from "./types"

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

export const sortFares = (fares: fare[]) => {
    const res = fares
    for (let i = 0; i < res.length; i++) {
        let minPrice = 9999
        let minIndex = i
        for (let j = i + 1; j < res.length; j++) {
            if (res[j].Price < minPrice) {
                minIndex = j
                minPrice = res[j].Price
            }
        }
        if (minIndex !== i) {
            const temp = res[i]
            res[i] = res[minIndex]
            res[minIndex] = temp
        }
    }
    return res
}