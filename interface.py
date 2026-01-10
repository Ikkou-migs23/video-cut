import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import time
import os

# ========== FUNÇÃO ORIGINAL DO CORTE (NÃO ALTERADA) ==========
def cortar_video(nome_dos_cortes, caminho_video_original, caminho_video_corte, progress_callback=None, log_callback=None):
    """
    Função original de corte de vídeo, adaptada para usar callbacks
    em vez de print/input diretos.
    """
    def log(msg):
        if log_callback:
            log_callback(msg)
        else:
            print(msg)
    
    try:
        from moviepy import VideoFileClip, TextClip, CompositeVideoClip
        
        # constantes
        video = VideoFileClip(caminho_video_original)
        duracao_total = video.duration
        duracao_corte = 60
        numero_cortes = int(duracao_total // duracao_corte)
        
        log(f"Iniciando os {numero_cortes} cortes")
        
        if progress_callback:
            progress_callback(0, numero_cortes + 1)  # +1 para a sobra
        
        # loop para a produção dos cortes:
        for i in range(numero_cortes):
            inicio = i * duracao_corte
            fim = inicio + duracao_corte
            
            log(f"Corte {i+1}/{numero_cortes}")
            
            # carregar o video original dentro do loop a cada corte:
            video_original = VideoFileClip(caminho_video_original)
            
            # criar os cortes
            corte = video_original.subclipped(inicio, fim)
            
            # salvar
            corte.write_videofile(os.path.join(caminho_video_corte, f"{nome_dos_cortes}_{i+1:03d}.mp4"))
            
            # Liberar memória
            corte.close()
            video_original.close()
            
            # Atualizar progresso
            if progress_callback:
                progress_callback(i + 1, numero_cortes + 1)
            
            # Esperar 2 segundos
            if i < numero_cortes - 1:  # Não esperar após o último
                log("Aguardando 2 segundos...")
                time.sleep(2)
            log("Cortes realizados")
        
        # Ultima etapa, pegar o ultimo corte (podemos chamar de sobra)
        tempo_total_cortes = duracao_corte * numero_cortes
        
        # Verificar se há sobra
        if tempo_total_cortes < duracao_total:
            inicio = tempo_total_cortes
            fim = duracao_total
            
            # carregar o video original dentro do loop a cada corte:
            video_original = VideoFileClip(caminho_video_original)
            
            # criar os cortes
            corte = video_original.subclipped(inicio, fim)
            
            # salvar
            corte.write_videofile(os.path.join(caminho_video_corte, f"{nome_dos_cortes}_sobra.mp4"))
            
            # Liberar memória
            corte.close()
            video_original.close()
            
            log("Corte da sobra realizada")
            
            # Atualizar progresso final
            if progress_callback:
                progress_callback(numero_cortes + 1, numero_cortes + 1)
        
        log("Todos os cortes concluídos!")
        return True
        
    except Exception as e:
        log(f"ERRO: {str(e)}")
        return False

# ========== INTERFACE GRÁFICA ==========
class VideoCutterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração da janela
        self.title("Cortador de Vídeos")
        self.geometry("500x600")
        
        # Variáveis de controle
        self.processing = False
        self.cancel_requested = False
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Criar interface
        self.create_widgets()
        
    def create_widgets(self):
        # Título
        self.title_label = ctk.CTkLabel(
            self, 
            text="✂️ Cortador de Vídeos", 
            font=("Arial", 24, "bold")
        )
        self.title_label.pack(pady=20)
        
        # Frame para entradas
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Nome dos cortes
        self.name_label = ctk.CTkLabel(
            self.input_frame, 
            text="Nome dos cortes:",
            font=("Arial", 14)
        )
        self.name_label.pack(pady=(10, 5))
        
        self.name_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Ex: meu_video",
            width=400
        )
        self.name_entry.pack(pady=5, padx=20)
        
        # Caminho do vídeo original
        self.original_label = ctk.CTkLabel(
            self.input_frame,
            text="Vídeo original:",
            font=("Arial", 14)
        )
        self.original_label.pack(pady=(10, 5))
        
        self.original_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.original_frame.pack(pady=5, padx=20, fill="x")
        
        self.original_entry = ctk.CTkEntry(
            self.original_frame,
            placeholder_text="Caminho completo do vídeo...",
            width=320
        )
        self.original_entry.pack(side="left", fill="x", expand=True)
        
        self.original_button = ctk.CTkButton(
            self.original_frame,
            text="📁",
            width=50,
            command=self.browse_original
        )
        self.original_button.pack(side="right", padx=(5, 0))
        
        # Caminho para salvar
        self.save_label = ctk.CTkLabel(
            self.input_frame,
            text="Salvar em:",
            font=("Arial", 14)
        )
        self.save_label.pack(pady=(10, 5))
        
        self.save_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.save_frame.pack(pady=5, padx=20, fill="x")
        
        self.save_entry = ctk.CTkEntry(
            self.save_frame,
            placeholder_text="Pasta para salvar os cortes...",
            width=320
        )
        self.save_entry.pack(side="left", fill="x", expand=True)
        
        self.save_button = ctk.CTkButton(
            self.save_frame,
            text="📁",
            width=50,
            command=self.browse_save
        )
        self.save_button.pack(side="right", padx=(5, 0))
        
        # Barra de progresso
        self.progress_label = ctk.CTkLabel(
            self,
            text="Pronto para começar",
            font=("Arial", 12)
        )
        self.progress_label.pack(pady=(20, 5))
        
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)
        
        # Área de log
        self.log_label = ctk.CTkLabel(
            self,
            text="Log de execução:",
            font=("Arial", 14)
        )
        self.log_label.pack(pady=(20, 5))
        
        self.log_text = ctk.CTkTextbox(self, width=450, height=150)
        self.log_text.pack(pady=5)
        
        # Botões
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)
        
        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="▶️ INICIAR CORTES",
            font=("Arial", 16, "bold"),
            width=200,
            height=40,
            command=self.start_cutting
        )
        self.start_button.pack(side="left", padx=10)
        
        self.cancel_button = ctk.CTkButton(
            self.button_frame,
            text="❌ CANCELAR",
            font=("Arial", 14),
            width=150,
            height=40,
            state="disabled",
            command=self.cancel_cutting
        )
        self.cancel_button.pack(side="right", padx=10)
        
    def browse_original(self):
        filetypes = [
            ("Vídeos", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv"),
            ("Todos os arquivos", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="Selecionar vídeo original",
            filetypes=filetypes
        )
        if filename:
            self.original_entry.delete(0, "end")
            self.original_entry.insert(0, filename)
    
    def browse_save(self):
        folder = filedialog.askdirectory(
            title="Selecionar pasta para salvar os cortes"
        )
        if folder:
            self.save_entry.delete(0, "end")
            self.save_entry.insert(0, folder)
    
    def log_message(self, message):
        """Adiciona uma mensagem ao log"""
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.update()
    
    def update_progress(self, current, total):
        """Atualiza a barra de progresso"""
        if total > 0:
            progress = current / total
            self.progress_bar.set(progress)
            self.progress_label.configure(
                text=f"Progresso: {current}/{total} ({progress*100:.1f}%)"
            )
    
    def start_cutting(self):
        """Inicia o processo de corte em uma thread separada"""
        # Validar entradas
        nome = self.name_entry.get().strip()
        original = self.original_entry.get().strip()
        save = self.save_entry.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Por favor, informe um nome para os cortes!")
            return
        
        if not original or not os.path.isfile(original):
            messagebox.showerror("Erro", "Por favor, selecione um vídeo original válido!")
            return
        
        if not save or not os.path.isdir(save):
            messagebox.showerror("Erro", "Por favor, selecione uma pasta de destino válida!")
            return
        
        # Limpar log anterior
        self.log_text.delete("1.0", "end")
        
        # Configurar interface para processamento
        self.start_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        self.processing = True
        self.cancel_requested = False
        
        # Iniciar thread de processamento
        thread = threading.Thread(
            target=self.process_video,
            args=(nome, original, save),
            daemon=True
        )
        thread.start()
    
    def process_video(self, nome, original, save):
        """Processa o vídeo em uma thread separada"""
        try:
            # Executar a função de corte original
            success = cortar_video(
                nome_dos_cortes=nome,
                caminho_video_original=original,
                caminho_video_corte=save,
                progress_callback=self.update_progress,
                log_callback=self.log_message
            )
            
            if success and not self.cancel_requested:
                self.after(0, lambda: messagebox.showinfo(
                    "Sucesso",
                    "Todos os cortes foram concluídos com sucesso!"
                ))
        
        except Exception as e:
            self.after(0, lambda: messagebox.showerror(
                "Erro",
                f"Ocorreu um erro durante o processamento:\n{str(e)}"
            ))
        
        finally:
            # Restaurar interface
            self.after(0, self.reset_interface)
    
    def cancel_cutting(self):
        """Cancela o processo em andamento"""
        self.cancel_requested = True
        self.cancel_button.configure(state="disabled")
        self.log_message("Processo cancelado pelo usuário...")
    
    def reset_interface(self):
        """Restaura a interface ao estado inicial"""
        self.start_button.configure(state="normal")
        self.cancel_button.configure(state="disabled")
        self.processing = False

# ========== EXECUÇÃO DO PROGRAMA ==========
if __name__ == "__main__":
    app = VideoCutterApp()
    app.mainloop()