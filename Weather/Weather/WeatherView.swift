//
//  WeatherView.swift
//  Weather
//
//  Created by John Jones on 2/19/22.
//

import SwiftUI

struct WeatherView: View {
    var weather: Weather
    
    var body: some View {
        let textColor = getTempColor(value: weather.temperature).text
        let shadowColor = getTempColor(value: weather.temperature).shadow
        return GeometryReader{ geo in
            ZStack{
                LinearGradient(
                    colors: [weather.topColor, weather.bottomCollor],
                    startPoint: .top,
                    endPoint: .bottom)
                    .edgesIgnoringSafeArea(.all)

                VStack(alignment: .center){
                    
                    Text(String(format: "%.f°", weather.temperatureF))
                        .font(Font.system(size: geo.size.height/4))
                        .frame(maxHeight: geo.size.height/5)
                        .foregroundColor(textColor)
                        .shadow(
                            color: shadowColor,
                            radius: 1,
                            x: 1,
                            y: 1
                        )
                    
                    verticalSeparator(geo: geo)
                    
                    ForEach(weather.iterableFeatures) { feature in
                        HStack{
                            Text("\(feature.label): ")
                                .font(.headline)
                                .frame(alignment: .leading)
                                .foregroundColor(textColor)
                                .shadow(
                                    color: shadowColor,
                                    radius: 0,
                                    x: 1,
                                    y: 1
                                )
                            Text(feature.value)
                                .frame(maxWidth: .infinity, alignment: .trailing)
                                .foregroundColor(textColor)
                                .shadow(
                                    color: shadowColor,
                                    radius: 0,
                                    x: 1,
                                    y: 1
                                )
                        }
                            .frame(width: geo.size.width * 0.9)
                            .padding(.top, geo.size.height * 0.01)
                    }
                    
                    verticalSeparator(geo: geo)
                        .padding(.top, geo.size.height * 0.01)
                    
                    Text("Reading taken \(weather.timeReadable).")
                        .font(.subheadline)
                        .padding(.top, geo.size.height * 0.01)
                        .foregroundColor(textColor)
                        .shadow(
                            color: shadowColor,
                            radius: 0,
                            x: 1,
                            y: 1
                        )
                }
                
                    .frame(maxHeight: .infinity)
                    .padding(.bottom, geo.size.height * 0.2)
            }
        }
    }
    
    func verticalSeparator(geo: GeometryProxy) -> some View {
        return Path() { path in
            path.move(to: CGPoint(x: geo.size.width * 0.05, y: 0))
            path.addLine(to: CGPoint(x: geo.size.width - (geo.size.width * 0.05), y: 0))
        }.stroke(getTempColor(value: weather.temperature).text, lineWidth: 1).frame(width: geo.size.width, height: 1, alignment: .center)
    }
}

struct IterableWeatherFeature: Identifiable {
    let label: String
    let value: String
    
    var id: String {
        return label
    }
}

extension Weather {
    var iterableFeatures: [IterableWeatherFeature] {
        return [
            IterableWeatherFeature(
                label: "Wind Speed",
                value: String(format: "%.2f MPH", self.avgWindSpeedMph)
            ),
            IterableWeatherFeature(
                label: "Humidity",
                value: String(format: "%.2f%%", self.relativeHumidity)
            ),
            IterableWeatherFeature(
                label: "Pressure",
                value: String(format: "%.2f inHg", self.pressureInHg)
            )
        ]
    }
    
    var avgWindSpeedMph: Double {
        return avgWindSpeed * 2.236936
    }
    
    var temperatureF: Double {
        return temperature * 1.8 + 32
    }
    
    var pressureInHg: Double {
        return pressure * 0.029530
    }
    
    var topColor: Color {
        return generateColors(value: temperature + 5)
    }
    
    var bottomCollor: Color {
        return generateColors(value: temperature - 5)
    }
    
    var timeReadable: String {
        let f = DateFormatter()
//        f.timeZone = TimeZone(abbreviation: "EST")
        f.dateStyle = .short
        f.timeStyle = .short
        return f.string(from: self.time)
    }
}

struct WeatherView_Previews: PreviewProvider {
    static var previews: some View {
        WeatherView(weather: Weather(
            timestamp: "2022-02-19T20:19:54.593207Z",
            avgWindSpeed: 0.5419089794158936,
            temperature:20,
            relativeHumidity: 22.808000564575195,
            pressure: 1018.0499877929688
        ))
    }
}
