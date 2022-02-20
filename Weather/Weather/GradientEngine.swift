//
//  GradientEngine.swift
//  Weather
//
//  Created by John Jones on 2/19/22.
//

import Foundation
import SwiftUI

struct TempColor {
    let value: Double
    let hexes: [Int]
    let text: Color
    let shadow: Color
}

extension Color {
    init(hexes: [Int]) {
        self.init(
            red: Double(hexes[0])/255.0,
            green: Double(hexes[1])/255.0,
            blue: Double(hexes[2])/255.0
        )
    }
}

let tempColors : [TempColor] = [
    TempColor(
        value: -10,
        hexes: [0xFF,
                0xFF,
                0xF9],
        text: Color.gray,
        shadow: Color(white: 0, opacity: 0.5)
    ),
    TempColor(
        value: 0,
        hexes: [0x47,
                0x98,
                0xF9],
        text: Color.white,
        shadow: Color(white: 0, opacity: 0.75)
    ),
    TempColor(
        value: 10,
        hexes: [0x09,
                0x7A,
                0xD3],
        text: Color.white,
        shadow: Color(white: 0, opacity: 0.75)
    ),
    TempColor(
        value: 20,
        hexes: [0xF9,
                0xAE,
                0x47],
        text: Color.white,
        shadow: Color(white: 0, opacity: 0.75)
    ),
    TempColor(
        value: 40,
        hexes: [0xF9,
                0x5F,
                0x47],
        text: Color.white,
        shadow: Color(white: 0, opacity: 0.75)
    )
]

func generateColors(value: Double) -> Color {
    if value <= tempColors.first!.value {
        return Color(hexes: tempColors.first!.hexes)
    }
    
    var lastColor = tempColors.first!
    for color in tempColors {
        if value <= color.value {
            let pcnt = (value - lastColor.value) / (color.value - lastColor.value)
            let hexes = color.hexes.enumerated().map { (i, h) in
                return lastColor.hexes[i] + Int(pcnt * Double(h - lastColor.hexes[i]))
            }
            return Color(hexes: hexes)
        } else {
            lastColor = color
        }
    }
    return Color(hexes: lastColor.hexes)
}

func getTempColor(value: Double) -> TempColor {
    var lastColor = tempColors.first!
    for color in tempColors {
        if value <= color.value {
            return color
        } else {
            lastColor = color
        }
    }
    return lastColor
}
