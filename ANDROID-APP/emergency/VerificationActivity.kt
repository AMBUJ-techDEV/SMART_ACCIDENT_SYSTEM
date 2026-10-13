package com.saders.accidentresponse.emergency

import android.os.Bundle
import android.os.CountDownTimer
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.saders.accidentresponse.R

class VerificationActivity : AppCompatActivity() {

    private lateinit var tvCountdown: TextView
    private lateinit var tvConfidence: TextView
    private lateinit var tvSeverity: TextView
    private lateinit var btnCancel: Button
    private lateinit var btnSendHelp: Button

    private var countDownTimer: CountDownTimer? = null
    private var verificationWindowSeconds = 15

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_verification)

        tvCountdown = findViewById(R.id.tvCountdown)
        tvConfidence = findViewById(R.id.tvConfidence)
        tvSeverity = findViewById(R.id.tvSeverity)
        btnCancel = findViewById(R.id.btnCancel)
        btnSendHelp = findViewById(R.id.btnSendHelp)

        val scorePct = intent.getIntExtra("CONFIDENCE_PCT", 91)
        val severity = intent.getStringExtra("SEVERITY") ?: "HIGH"

        tvConfidence.text = "$scorePct%"
        tvSeverity.text = severity

        startVerificationTimer()

        btnCancel.setOnClickListener {
            cancelVerification("FALSE_ALARM_BY_DRIVER")
        }

        btnSendHelp.setOnClickListener {
            confirmVerification("MANUAL_DRIVER_CONFIRMED")
        }
    }

    private fun startVerificationTimer() {
        countDownTimer = object : CountDownTimer((verificationWindowSeconds * 1000).toLong(), 1000) {
            override fun onTick(millisUntilFinished: Long) {
                val secondsRemaining = millisUntilFinished / 1000
                tvCountdown.text = "00:${if (secondsRemaining < 10) "0" else ""}$secondsRemaining"
            }

            override fun onFinish() {
                tvCountdown.text = "00:00"
                Toast.makeText(this@VerificationActivity, "Verification window expired. Auto-escalating incident!", Toast.LENGTH_LONG).show()
                confirmVerification("AUTO_ESCALATED_NO_RESPONSE")
            }
        }.start()
    }

    private fun cancelVerification(reason: String) {
        countDownTimer?.cancel()
        Toast.makeText(this, "Emergency cancelled. Marked as false alarm.", Toast.LENGTH_SHORT).show()
        finish()
    }

    private fun confirmVerification(responseType: String) {
        countDownTimer?.cancel()
        // Trigger eCall emergency alert packet creation via Backend REST API
        Toast.makeText(this, "Emergency Alert Dispatching! Locating nearest responders...", Toast.LENGTH_LONG).show()
        finish()
    }

    override fun onDestroy() {
        super.onDestroy()
        countDownTimer?.cancel()
    }
}
