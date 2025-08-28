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

class MainActivity : AppCompatActivity() {

    private lateinit var btnTirarFoto: Button
    private lateinit var imageView: ImageView

    // 1. Lançador para o resultado da CÂMERA
    @RequiresApi(Build.VERSION_CODES.TIRAMISU)
    private val resultLauncherCamera = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        if (result.resultCode == RESULT_OK) {
            val data: Intent? = result.data
            // Usando o método seguro que discutimos antes
            val imageBitmap = data?.extras?.getParcelable("data", Bitmap::class.java)
            imageView.setImageBitmap(imageBitmap)
        }
    }

    // 2. Lançador para o pedido de PERMISSÃO
    @RequiresApi(Build.VERSION_CODES.TIRAMISU)
    private val requestPermissionLauncher = registerForActivityResult(ActivityResultContracts.RequestPermission()) { isGranted: Boolean ->
        if (isGranted) {
            // Permissão concedida, podemos abrir a câmera
            abrirCamera()
        } else {
            // Permissão negada, mostramos uma mensagem ao usuário
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
            // 3. Ao clicar no botão, chamamos a função que verifica a permissão
            verificarPermissaoDaCamera()
        }
    }

    @RequiresApi(Build.VERSION_CODES.TIRAMISU)
    private fun verificarPermissaoDaCamera() {
        when {
            // Verifica se a permissão JÁ FOI CONCEDIDA
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.CAMERA
            ) == PackageManager.PERMISSION_GRANTED -> {
                // Se sim, abre a câmera diretamente
                abrirCamera()
            }

            else -> {
                // Se não, pede a permissão ao usuário
                requestPermissionLauncher.launch(Manifest.permission.CAMERA)
            }
        }
    }

    @RequiresApi(Build.VERSION_CODES.TIRAMISU)
    private fun abrirCamera() {
        val cameraIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        resultLauncherCamera.launch(cameraIntent)
    }
}