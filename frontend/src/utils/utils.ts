export const getNextThreeTrains = (trains: any) => {
    const now = new Date().toTimeString().slice(0,9)
    console.log(trains)
    let counter = 0
    let flag = false
    const nextThreeTrains = trains.filter((train: any) => {
        if (train.DepartureTime >= now) flag = true
        if (!flag || counter >= 3) return
        counter++
        return train.DepartureTime >= now
    })
    return nextThreeTrains
}