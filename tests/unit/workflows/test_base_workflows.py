import pytest

pytestmark = pytest.mark.workflow


def test_ksampler(default_workflow):
    assert default_workflow.ksampler == {
        "cfg": 7,
        "denoise": 1.0,
        "sampler_name": "euler",
        "scheduler": "simple",
        "seed": 42,
        "steps": 20,
    }


def test_latent_empty(default_workflow):
    assert default_workflow.latent_empty == {
        "batch_size": 1,
        "height": 512,
        "width": 512,
    }


def test_latent_image(default_workflow):
    assert default_workflow.latent_image == {"image": "blah"}


def test_workflow_to_dict(default_workflow):
    assert default_workflow.to_dict == {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": "mock.safetensors",
            },
        },
        "10": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": "ccc",
                "images": [
                    "6",
                    0,
                ],
            },
        },
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": [
                    "1",
                    1,
                ],
                "text": "cat with a hat",
            },
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": [
                    "1",
                    1,
                ],
                "text": "hands",
            },
        },
        "5": {
            "class_type": "KSampler",
            "inputs": {
                "cfg": 7,
                "denoise": 1.0,
                "latent_image": [
                    "8",
                    0,
                ],
                "model": [
                    "1",
                    0,
                ],
                "negative": [
                    "3",
                    0,
                ],
                "positive": [
                    "2",
                    0,
                ],
                "sampler_name": "euler",
                "scheduler": "simple",
                "seed": 42,
                "steps": 20,
            },
        },
        "6": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": [
                    "5",
                    0,
                ],
                "vae": [
                    "1",
                    2,
                ],
            },
        },
        "8": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "batch_size": 1,
                "height": 512,
                "width": 512,
            },
        },
    }
