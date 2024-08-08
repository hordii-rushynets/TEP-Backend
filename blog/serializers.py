from typing import OrderedDict

from rest_framework import serializers

from tep_user.models import TEPUserSocialNetworks

from .models import Post, Section, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title_uk', 'title_en', 'title_ru']


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'types', 'title_uk', 'title_en', 'title_ru', 'description_uk', 'description_en',
                  'description_ru', 'additional_description_uk', 'additional_description_en',
                  'additional_description_en', 'image')


class PostSerializer(serializers.ModelSerializer):
    tags = TagTitleSerializer(read_only=True, many=True)
    author = serializers.SerializerMethodField()
    section = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title_uk', 'title_en', 'title_ru', 'meta_description_uk', 'meta_description_en',
                  'meta_description_ru', 'slug', 'image', 'created_at', 'author', 'section', 'tags')

    def get_author(self, post: Post) -> dict:
        """Method to retrieve an infromation about social networks of post author."""
        social_networks = TEPUserSocialNetworks.objects.filter(user=post.author)

        author = {
            'name': post.author.full_name,
            'social_networks': {}
        }

        for social_network in social_networks:
            author['social_networks'][social_network.types] = social_network.url

        return author

    def to_representation(self, post: Post) -> OrderedDict:
        """
        This method overrides the default `to_representation` method to restructure the serialized
        output of the Post instance. Specifically, it processes the 'section' field such that the 
        'types' field of each section becomes a key in the representation. The original 'section' 
        field is removed from the final output.
        """
        representation = super().to_representation(post)
        for section in representation['section']:
            types = section.pop('types')
            representation[types] = section

        del representation['section']

        return representation
