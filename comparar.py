from skimage import io
from skimage.transform import resize
from skimage.metrics import structural_similarity as ssim

# Carregando a primeira imagem
img1 = io.imread('enhanced/img_login.png', as_gray=True)

# Lista das imagens para comparar
image_list = ['enhanced/img_1.png', 'enhanced/img_2.png', 'enhanced/img_3.png', 'enhanced/img_4.png', 'enhanced/img_5.png']

# Variáveis para armazenar a melhor SSIM e a melhor imagem
best_ssim = -1
best_image = ""

# Iterando sobre a lista de imagens
for image in image_list:
    img2 = io.imread(image, as_gray=True)
    img2_resized = resize(img2, img1.shape)
    ssim_index = ssim(img1, img2_resized, data_range=1.0)
    ssim_index = ssim_index * 100
    # Verificando se essa imagem tem a melhor SSIM até agora
    if ssim_index > best_ssim:
        best_ssim = ssim_index
        best_image = image

print(f'A imagem com a maior similaridade é {best_image} com SSIM: {best_ssim}')
