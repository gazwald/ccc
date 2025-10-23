from ccc.models.enums import NodeClassType as NCT
from ccc.models.enums import NodeID
from ccc.models.prompt import EmptyLatentImage
from ccc.models.types import KSampler, LatentImage


def noder(class_type: NCT, *args, **kwargs) -> dict:
    match class_type:
        case NCT.CLIPTextEncode:
            return clip_text_encode_noder(*args, **kwargs)
        case NCT.CheckpointLoaderSimple:
            return checkpoint_node(*args, **kwargs)
        case NCT.EmptyLatentImage:
            return empty_latent_image_node(*args, **kwargs)
        case NCT.KSampler:
            return ksampler_node(*args, **kwargs)
        case NCT.LoadImage:
            return load_image_node(*args, **kwargs)
        case NCT.SaveImage:
            return save_image_node(*args, **kwargs)
        case NCT.VAEDecodeTiled:
            return vae_decode_node(*args, **kwargs)
        case NCT.VAEEncodeTiled:
            return vae_encode_node(*args, **kwargs)
        case NCT.VAELoader:
            return vae_loader_node(*args, **kwargs)
        case _:
            return {}


def clip_text_encode_noder(*args, **kwargs) -> dict:
    sentiment: bool = kwargs.pop("sentiment", False)
    node_id: NodeID = NodeID.clip_text_pos_id if sentiment else NodeID.clip_text_neg_id
    return clip_text_encode_node(node_id, *args, **kwargs)


def checkpoint_node(checkpoint: str) -> dict:
    return {
        NodeID.checkpoint_id.value: {
            "inputs": {"ckpt_name": checkpoint},
            "class_type": "CheckpointLoaderSimple",
        }
    }


def vae_loader_node(vae: str) -> dict:
    return {
        NodeID.vae_id.value: {
            "inputs": {"vae_name": vae},
            "class_type": "VAELoader",
        }
    }


def clip_text_encode_node(node_id: NodeID, text: str) -> dict:
    return {
        node_id.value: {
            "inputs": {
                "text": text,
                "clip": [NodeID.checkpoint_id.value, 1],
            },
            "class_type": "CLIPTextEncode",
        }
    }


def ksampler_node(ksampler: KSampler) -> dict:
    return {
        NodeID.sampler_id.value: {
            "inputs": {
                **ksampler,
                "model": [NodeID.checkpoint_id.value, 0],
                "positive": [NodeID.clip_text_pos_id.value, 0],
                "negative": [NodeID.clip_text_neg_id.value, 0],
                "latent_image": [NodeID.empty_latent_id.value, 0],
            },
            "class_type": "KSampler",
        }
    }


def vae_decode_node() -> dict:
    return {
        NodeID.vae_decode_id.value: {
            "inputs": {
                "samples": [NodeID.sampler_id.value, 0],
                "vae": [NodeID.checkpoint_id.value, 2],
            },
            "class_type": "VAEDecode",
        }
    }


def vae_encode_node() -> dict:
    return {
        NodeID.vae_encode_id.value: {
            "inputs": {
                "tile_size": 512,
                "overlap": 64,
                "temporal_size": 8,
                "temporal_overlap": 8,
                "pixels": [NodeID.load_image_id.value, 0],
                "vae": [NodeID.vae_id.value, 0],
            },
            "class_type": "VAEEncodeTiled",
        }
    }


def load_image_node(latent_image: LatentImage) -> dict:
    return {
        NodeID.load_image_id.value: {
            "inputs": latent_image,
            "class_type": "LoadImage",
        }
    }


def empty_latent_image_node(empty_latent: EmptyLatentImage) -> dict:
    return {
        NodeID.empty_latent_id.value: {
            "inputs": empty_latent,
            "class_type": "EmptyLatentImage",
        }
    }


def save_image_node(prefix: str = "ccc") -> dict:
    return {
        NodeID.save_image_id.value: {
            "inputs": {
                "filename_prefix": prefix,
                "images": [NodeID.vae_decode_id.value, 0],
            },
            "class_type": "SaveImage",
        }
    }
