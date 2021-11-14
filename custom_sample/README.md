# Sample using vagrant-ansible-provisioner

Sample using a custom wrapper above `vagrant-ansible-provisioner`.

## How to use

Just type `python manage.py initialize --build`.

It's "prebuilt box" compatible, so you need to build the box and export it later.

## Export and use prebuilt box

Once the environment is up, you can export it using the `package-box` command, like this:

```bash
python ./manage.py package-box \
    custom-sample \
    ./prebuilt.box \
    --box-name local/custom-sample \
    --box-description "My box" \
    --box-version "1.0.0"
```

It will create a `prebuilt.box` and a `prebuilt.json` file.

To use the box, you need to import the JSON file, using the `install-box` command, like this:

```bash
python ./manage.py install-box ./prebuilt.json
```

It should print something like that:

```text
==> box: Loading metadata for box 'prebuilt.json'
    box: URL: file://C:/Users/User/custom_sample/prebuilt.json
==> box: Adding box 'local/custom-sample' (v1.0.0) for provider: virtualbox
    box: Downloading: ./prebuilt.box
    box:
    box: Calculating and comparing box checksum...
==> box: Successfully added box 'local/custom-sample' (v1.0.0) for 'virtualbox'!
```

Now, if you change your machine name, or destroy the existing machine (with `vagrant destroy`), you can use:

```bash
python manage.py initialize
```

It will create a machine based on your prebuilt box file.
