# FingerprintFeatureExtraction
As características importantes das minúcias da impressão digital são os pontos finais das cristas (também conhecidas como terminações) e as bifurcações das cristas.

![image](https://user-images.githubusercontent.com/13918778/35665327-9ddbd220-06da-11e8-8fa9-1f5444ee2036.png)

O conjunto de recursos para a imagem consiste na localização das terminações e bifurcações e suas orientações

## Instalação e execução dos testes

 ## metodo 1
 ```
  pip install fingerprint-feature-extractor
 ```
 
 **uso:**
  ```
  import fingerprint_feature_extractor
  img = cv2.imread('image_path', 0)				# read the input image --> You can enhance the fingerprint image using the "fingerprint_enhancer" library
  FeaturesTerminations, FeaturesBifurcations = fingerprint_feature_extractor.extract_minutiae_features(img, spuriousMinutiaeThresh=10, invertImage=False, showResult=True, saveResult=True)
```
 ## metodo 2
- da pasta src, execute o arquivo "main.py"
- **a imagem de entrada é armazenada na pasta "enhanced".**
***Se a imagem de entrada não for aprimorada, os recursos de minúcias serão muito ruidosos***

# Bibliotecas necessárias:
- opencv
- skimage
- numpy
- math

# Nota
use o código https://github.com/Utkarsh-Deshmukh/Fingerprint-Enhancement-Python para melhorar a imagem da impressão digital.
Este programa pega a imagem de impressão digital aprimorada e extrai os recursos minuciosos.

Aqui estão algumas das saídas:


![1](https://user-images.githubusercontent.com/13918778/35665568-ae1fdb6c-06db-11e8-937b-33d7445c931d.jpg)   ![enhanced_feat1](https://user-images.githubusercontent.com/13918778/35665578-baddaf82-06db-11e8-8638-d24de65acd31.jpg)


# Como combinar as minúcias extraídas?
Vários artigos são publicados para realizar correspondência de minúcias.
Aqui estão alguns bons:
- "ALGORITMOS DE CORRESPONDÊNCIA BASEADOS EM MINUTIAE EM SISTEMAS DE RECONHECIMENTO DE IMPRESSÕES DIGITAIS" por Łukasz WIĘCŁAW
http://www.keia.ath.bielsko.pl/sites/default/files/publikacje/11-BIO-41-lukaszWieclawMIT_v2_popr2.pdf

"Um algoritmo de correspondência de impressão digital baseado em minúcias usando correlação de fase" por Weiping Chen e Yongsheng Gao
https://core.ac.uk/download/pdf/143875633.pdf

"RECONHECIMENTO DE IMPRESSÕES DIGITAIS USANDO MINUTIA SCORE MATCHING" por RAVI. J, K. B. RAJA, VENUGOPAL. K. R
https://arxiv.org/ftp/arxiv/papers/1001/1001.4186.pdf

# ATUALIZADO 

# Extração e Comparação de Características de Impressões Digitais com Flask

Este projeto se trata da extração de características de impressões digitais e da comparação dessas características. Ele é escrito em Python e usa a biblioteca Flask para criar uma API web. O projeto consiste em dois arquivos principais:

- `example.py`, que extrai características de uma lista de imagens e as compara com uma imagem de referência, fornecendo a distância euclidiana dos pontos extraídos.
- `comparar.py`, que aceita duas imagens via uma requisição HTTP POST, extrai características das impressões digitais dessas imagens, compara essas características e retorna a similaridade entre as duas imagens como uma resposta HTTP.

## Instalação e Configuração

1. Clone o repositório para o seu espaço de trabalho
    ```shell
    git clone https://github.com/seu_usuario/seu_projeto.git
    cd seu_projeto
    ```
2. Crie um ambiente virtual (opcional, mas recomendado)
    ```shell
    python3 -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```
3. Instale as dependências necessárias
    ```shell
    pip install flask numpy opencv-python-headless pillow json
    ```

## Uso

Para usar este projeto, você pode seguir os passos abaixo.

### Sem Flask

Para rodar `example.py`:

```shell
python example.py
```
### Com Flask
Para rodar comparar.py:

```shell
python comparar.py
```
Isso irá iniciar um servidor Flask na porta 8000.

Para comparar duas imagens, você precisa enviar uma requisição POST para http://localhost:8000/compare com o corpo da requisição contendo duas imagens codificadas em base64 nos campos 'img1' e 'img2'. A API irá extrair características das imagens, compará-las e retornar a similaridade das imagens como resposta.

### Por exemplo, usando curl:

```shell
curl -X POST -d "img1=$(base64 -w 0 image1.png)&img2=$(base64 -w 0 image2.png)" http://localhost:8000/compare
```
Isso retornará a similaridade entre image1.png e image2.png.

## Função PHP

No metodo PHP abaixo, eu envio a imagem vinda do front-end onde faço a captura da digital, depois dentro do metodo realizo a leitura das imagens já salvas no banco de dados, e envio uma a uma dentro do loop junto com a primeira que é a base, e as demais vinda do banco, caso a porcentagem de similaridade esteja acima de 75% termina, aconselhavel enviar um outro argumento para que não percorra todas as imagens do banco.
```shell
    public function verify($image) {
       
        $imagesDb = $this->read(); ///imagens vinda do banco de dados, varias imagens
        $result['status'] = false;

            $base64_str = str_replace('data:image/png;base64,', '', $image);//imagem vinda do front-end
            $bin = base64_decode($base64_str);
            $size = getImageSizeFromString($bin);

            if (empty($size['mime']) || strpos($size['mime'], 'image/') !== 0) {
            die('Base64 value is not a valid image');
            }
            $ext = substr($size['mime'], 6);
            if (!in_array($ext, ['png', 'gif', 'jpeg'])) {
            die('Unsupported image type');
            }
            $img_login = "../../images/img_login.{$ext}";
            $size_login = $size[0];
            file_put_contents($img_login, $bin);
            $imagem=json_decode(json_encode($image), true);
            $soma=[];
            $i=0;
            foreach ($imagesDb as $users_file_b64) {
                $id =intval($users_file_b64['user_id']);
                $i++;
                $obs =$users_file_b64['obs'];
                $file_b64 =explode(',', $users_file_b64['bio']);
                $file_b64 = $file_b64[1];
                $bin2 = base64_decode($file_b64);
                $size2 = getImageSizeFromString($bin2);
                
                $img_banco = "../../images/img_{$i}.png";
                $size_banco = $size2[0];
                file_put_contents($img_banco, $bin2);


                $url = 'http://localhost:8000/compare';

                // Define the image data
                $post_data = http_build_query(array(
                    'img1' => base64_encode(file_get_contents($img_login)),
                    'img2' => base64_encode(file_get_contents($img_banco)),
                ));

                // Initialize a CURL session
                $ch = curl_init();
                curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/x-www-form-urlencoded',
                'Content-Type: multipart/form-data'));
                curl_setopt($ch, CURLOPT_URL, $url);
                curl_setopt($ch, CURLOPT_POST, true);
                curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);

                // Execute the CURL session
                $response = curl_exec($ch);

                // Get the HTTP status code of the CURL session
                $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

                // Close the cURL session
                curl_close($ch);

                // Parse the response
                $response_data = json_decode($response, true);

                $best_ssim = $response_data['ssim'];

                array_push($soma,$best_ssim);
                if($best_ssim >= 75){
                    $result['status'] = true;
                    $result['message'] = $best_ssim;
                    $result['imagem'] = $img_banco;
                    $result['obs'] = $obs;
                    echo json_encode($result);
                    exit;
                }  
            }   
            if(!empty($img_banc)){
                unlink($img_banco);
                unlink($img_login);
            }
            $result['status'] = false;
            $result['message'] = 'Dados não conferem, tente novamente!';
            $result['valores'] = $soma;
            echo json_encode($result);
            //imagedestroy($image1);
            //imagedestroy($image2);
            exit;
         
    }
```
