//
//  WeatherLoader.swift
//  Weather
//
//  Created by John Jones on 2/18/22.
//

import Foundation
import Combine

class WeatherLoader: ObservableObject {
    let url = URL(string: "http://jonesweather.s3-website-us-east-1.amazonaws.com/latest.json")
    private var subscribers = Set<AnyCancellable>()
    
    @Published var weather: Weather?
    
    func getWeather() {
        URLSession.shared.dataTaskPublisher(for: url!)
            .map{$0.data}
            .decode(type: Weather.self, decoder: JSONDecoder())
            .eraseToAnyPublisher()
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { (error) in
                    print(error)
                },
                receiveValue: {
                    self.weather = $0
                }
            )
            .store(in: &subscribers)
    }
}
