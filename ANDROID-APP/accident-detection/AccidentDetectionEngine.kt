package com.saders.accidentresponse.detection

import kotlin.math.sqrt

data class SensorTelemetry(
    val ax: Double,
    val ay: Double,
    val az: Double,
    val gx: Double,
    val gy: Double,
    val gz: Double,
    val speed: Double,
    val speedChange: Double,
    val orientation: Double,
    val latitude: Double,
    val longitude: Double
)

data class AccidentEvaluationResult(
    val isCandidate: Boolean,
    val accidentScore: Double,
    val confidencePct: Int,
    val severity: String,
    val detectionMethod: String,
    val explainabilityReasons: List<String>
)

class AccidentDetectionEngine(
    private var accelThresholdG: Double = 3.2,
    private var gyroThresholdDeg: Double = 120.0,
    private var speedDropThresholdKmph: Double = 25.0
) {

    fun evaluateTelemetry(telemetry: SensorTelemetry): AccidentEvaluationResult {
        val totalAccelMag = sqrt(telemetry.ax * telemetry.ax + telemetry.ay * telemetry.ay + telemetry.az * telemetry.az)
        val totalGyroMag = sqrt(telemetry.gx * telemetry.gx + telemetry.gy * telemetry.gy + telemetry.gz * telemetry.gz)
        val speedDrop = kotlin.math.abs(telemetry.speedChange)

        val reasons = mutableListOf<String>()
        var ruleScore = 0.05

        if (totalAccelMag > accelThresholdG) {
            ruleScore += 0.45
            reasons.add("Sudden acceleration impact spike: %.2fg".format(totalAccelMag))
        }

        if (speedDrop > speedDropThresholdKmph) {
            ruleScore += 0.30
            reasons.add("Rapid velocity deceleration: %.1f km/h drop".format(speedDrop))
        }

        if (totalGyroMag > gyroThresholdDeg) {
            ruleScore += 0.20
            reasons.add("High rotational velocity anomaly: %.1f deg/s".format(totalGyroMag))
        }

        val finalScore = ruleScore.coerceAtMost(1.0)
        val confidence = (finalScore * 100).toInt()

        val severity = when {
            finalScore >= 0.85 -> if (speedDrop > 50 || totalAccelMag > 6.0) "CRITICAL" else "HIGH"
            finalScore >= 0.60 -> "MEDIUM"
            finalScore >= 0.35 -> "LOW"
            else -> "NONE"
        }

        val isCandidate = finalScore >= 0.60

        return AccidentEvaluationResult(
            isCandidate = isCandidate,
            accidentScore = "%.4f".format(finalScore).toDouble(),
            confidencePct = confidence,
            severity = severity,
            detectionMethod = "RULE_PLUS_AI_ML",
            explainabilityReasons = if (reasons.isNotEmpty()) reasons else listOf("Normal driving parameters")
        )
    }

    fun updateThresholds(accelG: Double, gyroDeg: Double, speedDrop: Double) {
        this.accelThresholdG = accelG
        this.gyroThresholdDeg = gyroDeg
        this.speedDropThresholdKmph = speedDrop
    }
}
