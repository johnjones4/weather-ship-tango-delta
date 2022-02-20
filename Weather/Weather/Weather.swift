//
//  Weather.swift
//  Weather
//
//  Created by John Jones on 2/18/22.
//

import Foundation

struct Weather: Decodable {
    let timestamp: String
    let avgWindSpeed: Double
    let temperature: Double
    let relativeHumidity: Double
    let pressure: Double
    
    var time: Date {
        let RFC3339DateFormatter = DateFormatter()
        RFC3339DateFormatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ss.SSSxxx"
        return RFC3339DateFormatter.date(from: timestamp)!
    }
    
    enum CodingKeys: String, CodingKey {
        case timestamp
        case avgWindSpeed = "avg_wind_speed"
        case temperature
        case relativeHumidity = "relative_humidity"
        case pressure
    }
}

