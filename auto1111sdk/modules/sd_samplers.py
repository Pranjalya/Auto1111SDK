from . import sd_samplers_kdiffusion, sd_samplers_timesteps, shared

all_samplers = [
    *sd_samplers_kdiffusion.samplers_data_k_diffusion,
    *sd_samplers_timesteps.samplers_data_timesteps,
]
all_samplers_map = {x.name: x for x in all_samplers}

samplers = []
samplers_for_img2img = []
samplers_map = {}
samplers_hidden = {}


def find_sampler_config(name):
    if name is not None:
        config = all_samplers_map.get(name, None)
    else:
        config = all_samplers[0]

    return config


def create_sampler(name, model, tqdm_val):
    config = find_sampler_config(name)

    assert config is not None, f'bad sampler name: {name}'

    if model.is_sdxl and config.options.get("no_sdxl", False):
        raise Exception(f"Sampler {config.name} is not supported for SDXL")

    sampler = config.constructor(model, tqdm_val)
    sampler.config = config

    return sampler


def set_samplers():
    global samplers, samplers_for_img2img, samplers_hidden

    samplers_hidden = set([])
    samplers = all_samplers
    samplers_for_img2img = all_samplers

    samplers_map.clear()
    for sampler in all_samplers:
        samplers_map[sampler.name.lower()] = sampler.name
        for alias in sampler.aliases:
            samplers_map[alias.lower()] = sampler.name


def visible_sampler_names():
    return [x.name for x in samplers if x.name not in samplers_hidden]