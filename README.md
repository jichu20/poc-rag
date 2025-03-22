# RAG 

## Descripción
Este proyecto muestra un ejemplo sencillo de como podemos hacer un proceso de RAG con una base de datos chromaDB a partir de un frontal básico generado en gradio.


## Docker

### ChromaDb

Para arrancar chromadb en docker:

```sh
docker volume create chroma-data
docker run --rm -p 8001:8000 -v chroma-data:/chroma/chroma/ --name chromadb chromadb/chroma

# Arranque del contenedor en modo desatendido
docker run --rm -d -p 8001:8000 -v chroma-data:/chroma/chroma/ --name chromadb chromadb/chroma
```

Toda la información procesada será almacenada en el volumen de docker

