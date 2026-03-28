package com.cpa.cpasongs

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET

interface SongApiService {
    @GET("cpa/pages/songs.php")
    suspend fun getSongs(): List<Song>

    companion object {
        private const val BASE_URL = "http://10.0.2.2/" // Use 10.0.2.2 for localhost from Android emulator

        fun create(): SongApiService {
            return Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
                .create(SongApiService::class.java)
        }
    }
}
