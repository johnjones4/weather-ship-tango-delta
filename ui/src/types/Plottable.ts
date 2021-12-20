interface PlottableDataset {
  label: string
  data: number[]
}

export default interface Plottable {
  dates: Date[],
  data: PlottableDataset[]
}
