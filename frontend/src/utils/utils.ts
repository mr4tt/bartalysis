import { train, fare } from "./types"
import { DateTime } from "luxon";

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
        let minPrice = res[i].Price
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

export const updateTime = (time: string) => {
    if (time >= "13:00:00") {
        let parsedTime = DateTime.fromFormat(time, "HH:mm:ss");
        parsedTime = parsedTime.minus({ hours: 12 });
        let formattedTime = parsedTime.toFormat("HH:mm:ss");
        if (formattedTime < "10:00:00") {
            return formattedTime.slice(1, formattedTime.length - 3) + " pm";
        }
        return formattedTime.slice(0, formattedTime.length - 3) + " pm";
    } else if (time >= "12:00:00" && time < "13:00:00") {
        return time.slice(0, time.length - 3) + " pm";
    } else if (time >= "10:00:00") {
        return time.slice(0, time.length - 3) + " am"
    }
    return time.slice(1, time.length - 3) + " am"
}