package com.example.camera_project_app

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.os.Build
import android.os.Bundle
import android.provider.MediaStore
import android.widget.Button
import android.widget.ImageView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import java.io.ByteArrayOutputStream
import java.io.DataOutputStream
import java.net.Socket
import kotlin.concurrent.thread

class MainActivity : AppCompatActivity() {

    private lateinit var btnTirarFoto: Button
    private lateinit var imageView: ImageView

    private val SERVER_IP = "10.0.2.2" //  Coloque o IP do servidor
    private val SERVER_PORT = 5001     // Mesma porta do servidor Python



    @RequiresApi(Build.VERSION_CODES.TIRAMISU)
    private val resultLauncherCamera = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        if (result.resultCode == RESULT_OK) {
            val data: Intent? = result.data
            val imageBitmap = data?.extras?.getParcelable("data", Bitmap::class.java)
            imageView.setImageBitmap(imageBitmap)

            // Enviar a foto para o servidor
            if (imageBitmap != null) {
                enviarFotoParaServidor(imageBitmap)
            }
        }
    }

    @RequiresApi(Build.VERSION_CODES.TIRAMISU)
    private val requestPermissionLauncher = registerForActivityResult(ActivityResultContracts.RequestPermission()) { isGranted: Boolean ->
        if (isGranted) {
            abrirCamera()
        } else {
            Toast.makeText(this, "Permissão da câmera negada", Toast.LENGTH_SHORT).show()
        }
    }

    @RequiresApi(Build.VERSION_CODES.TIRAMISU)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        btnTirarFoto = findViewById(R.id.btnTirarFoto)
        imageView = findViewById(R.id.imageView)

        btnTirarFoto.setOnClickListener {
            verificarPermissaoDaCamera()
        }
    }

    @RequiresApi(Build.VERSION_CODES.TIRAMISU)
    private fun verificarPermissaoDaCamera() {
        when {
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.CAMERA
            ) == PackageManager.PERMISSION_GRANTED -> {
                abrirCamera()
            }
            else -> {
                requestPermissionLauncher.launch(Manifest.permission.CAMERA)
            }
        }
    }

    @RequiresApi(Build.VERSION_CODES.TIRAMISU)
    private fun abrirCamera() {
        val cameraIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        resultLauncherCamera.launch(cameraIntent)
    }

    // Função para enviar a foto para o servidor Python
    private fun enviarFotoParaServidor(bitmap: Bitmap) {
        Thread {
            try {
                // 1. Converte para bytes
                val stream = ByteArrayOutputStream()
                bitmap.compress(Bitmap.CompressFormat.JPEG, 90, stream)
                val imageBytes = stream.toByteArray()

                // 2. Conecta ao servidor usando IP e Porta configurados
                val socket = Socket(SERVER_IP, SERVER_PORT)
                val out = DataOutputStream(socket.getOutputStream())

                // 3. Envia tamanho (4 bytes) + imagem
                out.writeInt(imageBytes.size)
                out.write(imageBytes)
                out.flush()

                socket.close()
                runOnUiThread {
                    Toast.makeText(this, "Foto enviada com sucesso!", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                e.printStackTrace()
                runOnUiThread {
                    Toast.makeText(this, "Erro ao enviar: ${e.message}", Toast.LENGTH_LONG).show()
                }
            }
        }.start()
    }
