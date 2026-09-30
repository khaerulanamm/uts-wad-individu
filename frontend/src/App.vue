<template>
  <div class="container">
    <h1>🚌 Pemesanan Shuttle Kampus</h1>

    <!-- FORM CREATE -->
    <div class="card">
      <h2>Tambah Sesi Pemesanan</h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label>Nama Penumpang:</label>
          <input v-model="form.passenger_name" type="text" placeholder="Contoh: Ahmad Pratama" />
          <span v-if="errors.passenger_name" class="error-text">{{ errors.passenger_name }}</span>
        </div>

        <div class="form-group">
          <label>Rute:</label>
          <input v-model="form.route" type="text" placeholder="Contoh: Rektorat - Asrama Putra" />
          <span v-if="errors.route" class="error-text">{{ errors.route }}</span>
        </div>

        <div class="form-group">
          <label>Waktu Keberangkatan:</label>
          <input v-model="form.departure_time" type="text" placeholder="YYYY-MM-DD HH:MM" />
          <span v-if="errors.departure_time" class="error-text">{{ errors.departure_time }}</span>
        </div>

        <div class="form-group">
          <label>Nomor Kursi:</label>
          <input v-model.number="form.seat_number" type="number" min="1" />
          <span v-if="errors.seat_number" class="error-text">{{ errors.seat_number }}</span>
        </div>

        <button type="submit" class="btn-primary">Simpan Pemesanan</button>
      </form>
    </div>

    <!-- PENCARIAN -->
    <div class="search-bar">
      <input
        v-model="searchQuery"
        @input="onSearch"
        type="text"
        placeholder="Cari berdasarkan nama atau rute..."
      />
    </div>

    <!-- STATE 1: LOADING -->
    <div v-if="state === 'loading'" class="status-box">
      <p>⏳ Memuat data sesi shuttle...</p>
    </div>

    <!-- STATE 2: ERROR + RETRY -->
    <div v-else-if="state === 'error'" class="status-box error-box">
      <p>⚠️ Gagal mengambil data dari server: {{ errorMessage }}</p>
      <button @click="fetchSessions" class="btn-retry">🔄 Coba Lagi (Retry)</button>
    </div>

    <!-- STATE 3: IDLE / KOSONG -->
    <div v-else-if="state === 'success' && sessions.length === 0" class="status-box">
      <p>Aplikasi siap. Tidak ada data sesi yang ditemukan.</p>
    </div>

    <!-- STATE 4: SUCCESS (MENAMPILKAN DATA) -->
    <div v-else-if="state === 'success'" class="card">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nama Penumpang</th>
            <th>Rute</th>
            <th>Waktu</th>
            <th>Kursi</th>
            <th>Status</th>
            <th>Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in sessions" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.passenger_name }}</td>
            <td>{{ item.route }}</td>
            <td>{{ item.departure_time }}</td>
            <td>#{{ item.seat_number }}</td>
            <td><span :class="'badge ' + item.status.toLowerCase()">{{ item.status }}</span></td>
            <td>
              <button @click="confirmDelete(item.id)" class="btn-danger">Hapus</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- PAGINATION -->
      <div class="pagination">
        <button :disabled="page <= 1" @click="changePage(page - 1)">Previous</button>
        <span>Halaman {{ page }} dari {{ totalPages }}</span>
        <button :disabled="page >= totalPages" @click="changePage(page + 1)">Next</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export default {
  data() {
    return {
      sessions: [],
      state: 'idle',
      errorMessage: '',
      page: 1,
      limit: 5,
      total: 0,
      searchQuery: '',
      form: {
        passenger_name: '',
        route: '',
        departure_time: '',
        seat_number: 1,
        status: 'Booked'
      },
      errors: {}
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.total / this.limit) || 1;
    }
  },
  mounted() {
    this.fetchSessions();
  },
  methods: {
    async fetchSessions() {
      this.state = 'loading';
      this.errorMessage = '';
      try {
        const response = await axios.get(`${API_BASE_URL}/sessions`, {
          params: {
            page: this.page,
            limit: this.limit,
            search: this.searchQuery
          }
        });
        this.sessions = response.data.data;
        this.total = response.data.total;
        this.state = 'success';
      } catch (err) {
        this.state = 'error';
        this.errorMessage = err.message || 'Terjadi kesalahan koneksi';
      }
    },
    onSearch() {
      this.page = 1;
      this.fetchSessions();
    },
    changePage(newPage) {
      this.page = newPage;
      this.fetchSessions();
    },
    validateForm() {
      this.errors = {};
      if (!this.form.passenger_name.trim()) this.errors.passenger_name = 'Nama wajib diisi.';
      if (!this.form.route.trim()) this.errors.route = 'Rute wajib diisi.';
      if (!this.form.departure_time.trim()) this.errors.departure_time = 'Waktu wajib diisi.';
      if (!this.form.seat_number || this.form.seat_number <= 0) this.errors.seat_number = 'Nomor kursi minimal 1.';
      return Object.keys(this.errors).length === 0;
    },
    async submitForm() {
      if (!this.validateForm()) return;

      try {
        await axios.post(`${API_BASE_URL}/sessions`, this.form);
        alert('Sesi pemesanan berhasil ditambahkan!');
        this.form = { passenger_name: '', route: '', departure_time: '', seat_number: 1, status: 'Booked' };
        this.fetchSessions();
      } catch (err) {
        alert('Gagal menyimpan data: ' + (err.response?.data?.detail || err.message));
      }
    },
    async confirmDelete(id) {
      if (confirm(`Apakah Anda yakin ingin menghapus pemesanan dengan ID #${id}?`)) {
        try {
          await axios.delete(`${API_BASE_URL}/sessions/${id}`);
          alert('Pemesanan berhasil dihapus.');
          this.fetchSessions();
        } catch (err) {
          alert('Gagal menghapus data: ' + err.message);
        }
      }
    }
  }
};
</script>

<style>
.container { max-width: 900px; margin: 0 auto; padding: 20px; font-family: sans-serif; }
.card { background: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #ddd; }
.form-group { margin-bottom: 15px; display: flex; flex-direction: column; }
.form-group input { padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; }
.error-text { color: red; font-size: 12px; margin-top: 4px; }
.search-bar input { width: 100%; padding: 10px; margin-bottom: 20px; box-sizing: border-box; }
.status-box { padding: 15px; border-radius: 6px; text-align: center; background: #e0e0e0; margin-bottom: 20px; }
.error-box { background: #fde8e8; color: #900; border: 1px solid #f8b4b4; }
.btn-primary { background: #007bff; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; }
.btn-danger { background: #dc3545; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; }
.btn-retry { background: #ffc107; border: none; padding: 8px 12px; cursor: pointer; margin-top: 10px; border-radius: 4px; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
.pagination { display: flex; justify-content: space-between; align-items: center; margin-top: 15px; }
</style>