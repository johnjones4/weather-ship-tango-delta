//
//  ContentView.swift
//  Weather
//
//  Created by John Jones on 2/18/22.
//

import SwiftUI

struct ContentView: View {
    @ObservedObject var loader = WeatherLoader()
    let timer = Timer.publish(every: 60, on: .main, in: .common).autoconnect()
    
    var body: some View {
        return GeometryReader{ geo in
            loader.weather == nil ?
            AnyView(Text("Loading")) :
            AnyView(WeatherView(weather: loader.weather!))
        }
        .onAppear() {
            loader.getWeather()
        }
        .onReceive(timer) { _ in
            loader.getWeather()
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
.previewInterfaceOrientation(.portraitUpsideDown)
    }
}
