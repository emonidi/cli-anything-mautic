from setuptools import setup, find_namespace_packages

setup(
	name="cli-anything-mautic",
	version="1.0.0",
	packages=find_namespace_packages(include=["cli_anything.*"]),
	install_requires=[
		"click>=8.0.0",
		"prompt-toolkit>=3.0.0",
		"requests>=2.28.0",
	],
	python_requires=">=3.10",
	entry_points={
		"console_scripts": [
			"cli-anything-mautic=cli_anything.mautic.mautic_cli:main",
			"cli-anything=cli_anything.commands:main",
		],
	},
	package_data={
		"cli_anything.mautic": ["skills/*.md", "*.md"],
	},
)
